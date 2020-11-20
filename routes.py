from starlette.templating import Jinja2Templates
from starlette.requests import Request
from starlette.responses import Response
from starlette.staticfiles import StaticFiles
from starlette.responses import PlainTextResponse
from starlette.responses import RedirectResponse
from starlette.datastructures import QueryParams
import app


# My extras
import httpx
import html
import pandas as pd
#import numpy as np
import datetime
from pandas.tseries.offsets import BDay
from typing import Tuple, Type
import pickle
from pathlib import Path
from norway import Norway
import korona
import multipart

# Set html template dir
templates = Jinja2Templates(directory='templates')

# Setup peristent user lang variable
class LanguageTracker():
    def __init__(self):
        self.active = 'norsk'

try:
    user_lang.active
except:
    user_lang = LanguageTracker()

# Template languages
def get_language_settings() -> Tuple[LanguageTracker, list, str, int]:
    """
    Returns list of languages
    Returns string for "Change language"
    And finally, cound of languages
    """
    try:
        user_lang.active
    except:
        user_lang = LanguageTracker()

    if user_lang.active == "english":
        l_list = ["Norwegian", "English", "Languages"]
        selector ="Language"
    else:
        # put Norwegian in else as fallback
        l_list = [ "Norsk", "Engelsk", "Ditt språk" ]
        selector = "Endre språk"
        #l_list = ["Norsk"] # debug override

    l_list = [ "Norsk" ] # debug
    l_num = len(l_list)
    return (user_lang, l_list, selector, l_num)


def get_template_vars() -> Tuple[korona.Session, dict]:
    """ Output default template vars for jinja """

    # Language settins
    user_lang, lang, selector, langs = get_language_settings()

    # Date/timestamps
    s = korona.app_verify_setup()
    today = s.datapoints[0]
    updated = today
    nordate = today
    if user_lang.active == "norsk":
        nordate = korona.norwegian_date(today, True)

    init_dict = {
                 "head_title": "korona.kommune.nu",
                 "updated": updated,
                 "nordate": nordate,
                 "hero_title": "korona . kommune . nu",
                 "hero_link": "/",
                 "hero_subtitle": "Dagsaktuelle tall for ditt hjemsted",
                 "html_lang": lang,
                 "lang_selector": selector,
                 "languages": langs
                 }

    return (s, init_dict)

#async def user(request):
#    req = request.path_params['user_id']
#    print(req)
#    return PlainTextResponse(f"OK ?> requested = {req}")

async def subdomain_kommune(kid, request):
    """
    Deals with it
    For full commentary see fritekst()
    """

    # Debug
    print(f"got request = {request}")
    print(dir(request))

    print(request.url)

    data, skipped_items = korona.app_query([kid])
    _kingdom = data.pop('0000')
    s, response_dat = get_template_vars()
    hero_title = data[list(data.keys())[0]]['name']
    head_title = f"Korona-status for {hero_title}"
    hero_link = data[list(data.keys())[0]]['url']
    subtitle = data[list(data.keys())[0]]['alt']
    hero_subtitle = "Tall for din kommune "
    if subtitle:
        hero_subtitle = data[list(data.keys())[0]]['alt']
    response_dat.update(
        {
            "hero_link": hero_link,
        }
    )

    # Build response dict
    response_dat.update(
                    {
                    "request": request,
                    "head_title": head_title,
                    "hero_title": hero_title,
                    "hero_subtitle": hero_subtitle,
                    "skipped_items": skipped_items,
                    "result_dict": data,
                    "only_one": True,
                    "exactly_two": False
                    }
    )

    return templates.TemplateResponse('table.t', response_dat)




async def hjem(request):
    # fetch minimal data
    s, response_dat = get_template_vars()
    today = s.datapoints[0]

    # check subdomain
    full_url = str(request.url)
    subdomain = full_url.split(sep="//")[1].split(sep=".")[0].lower()
    if subdomain in ["korona", "din", "om", "www"]:
        if subdomain == "om":
            response = RedirectResponse(url='/om')
        elif subdomain == "sjekk":
            response = RedirectResponse(url='/utvalg')
    else:
        items, item_type = korona.app_get_items([subdomain])
        if len(items) == 1:
            if item_type == 0:
                await subdomain_kommune(items[0], request)
            elif item_type == 1:
                return RedirectResponse(url=f'/f/{items[0]}')
            else:
                return RedirectResponse(url=f'/sok/?sok={items[0]}')

    try:
        response_dat.update(s.book['ro']['0000'][today])
    except KeyError:
        response_dat.update(
                    {
                    'diff_n': 'NA', # number of new infected people last 24 hrs
                    'infected': 'NA', # muncipalities with infected (bool)
                    'green': 'NA', # muncipalities
                    'orange': 'NA',
                    'red': 'NA'
                   }
        )

    # construct rest of index vars
    response_dat.update({"request": request})

    # Return index template with vars
    return templates.TemplateResponse('index.t', response_dat)



async def fritekst(request):
    await request.form()
    try:
        # print(request.query_params.keys())
        ui = html.escape(request.query_params['sok'])
    except:
        # could not get input ..? => bail!
        response = RedirectResponse(url='/')
    else:
        ui = ui.replace("!  ","").replace("\\","").replace("/","")
        uinput = ui

        # create response dict for template
        s, response_dat = get_template_vars()
        # print(f"current = '{uinput}'")
        sammenslaatt = s.norge.sammenslaatt()

        if uinput.lower() in sammenslaatt:
            uinput = uinput.split(sep=",")
        else:
            # tillatt folk å bruke "og"
            uinput.replace(" ",",")
            uinput = [ y for x in uinput.split(sep=",") for y in x.split(sep=",og,")]

        #print(f"current = '{uinput}'")

        # Nota bene, enkelte søk fungerer ikke:
        # Oslo, Bergen, og Lavangen gir ...?
        # Oslo, Bergen og Lavangen gir Lavangen
        # Oslo og Bergen og Lavangen
        # Oslo og Lavangen, Bergen
        # Oslo,Bergen,Lavangen




    # Check that we have input
    items_to_display, query_type = korona.app_get_items(uinput)

    #rint(f"debug to_fetch={items_to_display}")
    #print(f"query_type={query_type}")

    if len(items_to_display) > 0:
        # Fetch data
        data, skipped_items = korona.app_query(items_to_display)

        # Test data
        # Note: skipped items are VERIFIED keys (and pertinent!)
        # data = dict
        # skipped_items = list
        # items_skipped = bool
        # returned_items = int, number of records per request
        items_skipped = True if skipped_items else False

        # Removing the kingdom from hits
        _kingdom = data.pop('0000')
        returned_items = len(data.keys())
        #print(f"debug returned_items = {returned_items}")


        if len(skipped_items) == len(items_to_display):
            # error-show: no data
            response = RedirectResponse(url='/') # TBD
        elif returned_items == 0:
            # error no_data (no query hits either..?)
            response = RedirectResponse(url='/') # TBD

        # template toggle bools
        only_one = True if returned_items == 1 else False
        exactly_two = True if returned_items == 2 else False

        #print(f"DEBUG response_dat= {response_dat}")


        # default header
        head_title = "sjekk.kommune.nu"
        hero_title = "sjekk.kommune.nu"
        hero_subtitle = "Aktulle tall for ditt søk"

        if only_one:
            hero_title = data[list(data.keys())[0]]['name']
            head_title = f"Korona-status for {hero_title}"
#            hero_title = data[list(data.keys())[0]]['url']
            hero_link = data[list(data.keys())[0]]['url']
            subtitle = data[list(data.keys())[0]]['alt']
            hero_subtitle = "Tall for din kommune "
            if subtitle:
                hero_subtitle = data[list(data.keys())[0]]['alt']

            response_dat.update(
                {
                    "hero_link": hero_link,
                }

            )
        elif exactly_two:
            kom_1 = data[list(data.keys())[0]]['name']
            kom_2 = data[list(data.keys())[1]]['name']
            hero_subtitle = f"{kom_1} og {kom_2}"
            head_title = f"Korona-status for {kom_1} og {kom_2}"
        else:
            n_of_n = f"{returned_items}/{len(items_to_display)}"
            nordate = response_dat['nordate']
            hero_subtitle = f"Viser {n_of_n} treff fra oppslag (data fra {nordate})"

        # make a custom hero
        if query_type == 1:
            q = uinput[0].capitalize()
            if " og " in q:
                a, b = uinput[0].split(sep=" og ")
                q = f"{a.capitalize()} og {b.capitalize()}"

            #print(f"q in {q}")
            if q in s.norge.fylker.keys():
                hero_title = f"Aktuelle tall for {q}"
            else:
                fylke = None
                for k, v in s.norge.alt_name.items():
                    for subkey in v.split(sep=" - "):
                        if q.lower() in subkey.lower():
                            hero_subtitle = v
                            hero_title = f"Aktuelle tall for {k}"
        elif query_type == 2:
            try:
                hero_title = s.custom_queries[uinput[0]]['title']
                hero_subtitle = s.custom_queries[uinput[0]]['subtitle']
                head_title = f"sjekk.kommune.nu - {uinput[0]}"
            except Exception as e:
                print(f"debug e={e}")
                pass

        # Build response dict
        response_dat.update(
                        {
                        "request": request,
                        "head_title": head_title,
                        "hero_title": hero_title,
                        "hero_subtitle": hero_subtitle,
                        "skipped_items": skipped_items,
                        "result_dict": data,
                        "only_one": only_one,
                        "exactly_two": exactly_two
                        }
        )

        return templates.TemplateResponse('table.t', response_dat)


    # display Could not find <your stupid query>
    return PlainTextResponse(f"Kunne ikke finne: <{uinput}>")


async def om_tjenesten(request):
    """ Om tjenesten, om tallene, om kildekode """
    #print(f"debug {dir(request)}")
    #for k,v in request.items():
    #    print(f"{k}={v}")

    #my_data = request['headers']
    #print(f"got: {my_data}")

    #test = request['headers'][0][1].decode('UTF-8').split(sep=".")
    #print(test)
    #print(request.url)

    subtitle = "Kjapp oversikt med tall fra FHI"
    s, response_dat = get_template_vars()
    response_dat.update(
        {
            "request": request,
            "head_title": "Om kommune.nu",
            "hero_link": "/om",
            "hero_title": "Om kommune.nu",
            "hero_subtitle": subtitle,
        }
    )
    return templates.TemplateResponse('about.t', response_dat)

async def utvalg(request):
    # get language settings
    s, response_dat = get_template_vars()

    # Individual muncipalities by fylke
    try:
        big_list = s.list_of_muncipalities
    except:
        big_list = {}
        for f, klist in s.norge.fylker.items():
            big_list[f] = []
            for k in klist:
                kid = s.norge.id[k]
                url = s.norge.data[kid]['url']
                big_list[f].append((k, kid, url))

        s.list_of_muncipalities = big_list

    #print(f"debug = {big_list}")
    #print(f"request is {request}")

    response_dat.update(
        {
            "request": request,
            "head_title": "korona.kommune.nu sp&oslash;rring",
            "hero_subtitle": "sjekk.kommune.nu",
            "hero_link": "/utvalg",
            "fylker": big_list,
            "utvalg": 0
        }
    )
    return templates.TemplateResponse('utvalg.t', response_dat)

async def utvalg_fylker(request):
    if request.method == "POST":
        data = await request.form()
        #print("debug data here")
        #print(data)

        return PlainTextResponse(f"{data}")

        # Concoct a list object from FormData dict
        uinput = []

        # Check that we have input
        items_to_display = korona.app_get_items(uinput)

        #print(f"debug to_fetch={items_to_display}")

        # Fetch data if any
        if len(items_to_display) > 0:
            data, skipped_items = korona.app_query(items_to_display)

        else:
            # TBD
            # return to utvalg_fyllker with a 302 redirect
            # but perhaps with an error message?
            # can use notification from bulma css

            return PlainTextResponse("No data found.")

    else:
        # get language settings
        s, response_dat = get_template_vars()

        # Individual muncipalities by fylke
        try:
            big_list = s.list_of_muncipalities
        except:
            big_list = {}
            for f, klist in s.norge.fylker.items():
                big_list[f] = []
                for k in klist:
                    kid = s.norge.id[k]
                    url = s.norge.data[kid]['url']
                    big_list[f].append((k, kid, url))

            s.list_of_muncipalities = big_list

        #print(f"debug = {big_list}")
        #print(f"request is {request}")

        response_dat.update(
            {
                "request": request,
                "head_title": "korona.kommune.nu sp&oslash;rring",
                "hero_subtitle": "sjekk.kommune.nu",
                "hero_link": "/utvalg",
                "fylker": big_list,
                "utvalg": 1
            }
        )
        return templates.TemplateResponse('utvalg.t', response_dat)

async def custom_subdomain(request):
    return PlainTextResponse("LOL")

async def utvalg_egen(request):
    # get language settings
    s, response_dat = get_template_vars()

    # Individual muncipalities by fylke
    try:
        big_list = s.list_of_muncipalities
    except:
        big_list = {}
        for f, klist in s.norge.fylker.items():
            big_list[f] = []
            for k in klist:
                kid = s.norge.id[k]
                url = s.norge.data[kid]['url']
                big_list[f].append((k, kid, url))

        s.list_of_muncipalities = big_list

    #print(f"debug = {big_list}")
#    print(f"request is {request}")

    response_dat.update(
        {
            "request": request,
            "head_title": "korona.kommune.nu sp&oslash;rring",
            "hero_subtitle": "sjekk.kommune.nu",
            "hero_link": "/utvalg",
            "fylker": big_list,
            "utvalg": 2
        }
    )
    return templates.TemplateResponse('utvalg.t', response_dat)


async def sjekk(request):
    #print("in sjekk")
    #print(dir(request.form))
    return PlainTextResponse(f"lol = {request}")


#@app.route('/run', methods=['POST'])
async def endre_spraak(request):
    lang_req = html.escape(request.path_params['set_lang'])

    # setup stuff
    s, response_dat = get_template_vars()
    try:
        user_lang.active
    except:
        user_lang = LanguageTracker()


    # TODO "use the class" (Hans Gruber)
    lang_list = []
    lang_list += ['Norsk', 'Norwegian']
    lang_list += ['Engelsk', 'English']

    if lang_req in lang_list:
        user_lang.active = lang_req.lower()

    response = RedirectResponse(url='/')
    #return PlainTextResponse(f"OK ?> requested = {lang_req}") # debug


async def fylke(request):
    """ Let the norge.lookup method do the job """
    try:
        uinput = html.escape(request.path_params['fylke'])
    except:
        return RedirectResponse(url='/')
    else:
        return RedirectResponse(url=f"/sok/?sok={uinput}")


async def kommune(request):
    """ Let the norge.lookup method do the job """
    print(f"received {request.keys()}")
    try:
        uinput = html.escape(request.path_params['kom'])
    except:
        return RedirectResponse(url='/')
    else:
        return RedirectResponse(url=f"/sok/?sok={uinput}")


#@app.routes('/testing', methods=['POST'])
#async def ipn_post(request):
#    print('hi')
 #   print(request.form())

#async def confirmation(request):
#    return templates.TemplateResponse('confirmation.html', {'request': request})

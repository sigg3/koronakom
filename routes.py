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
from numpy import nan
#import numpy as np
import datetime
from pandas.tseries.offsets import BDay
import matplotlib.pyplot as plt
import seaborn as sns
import io
import base64
from typing import Tuple, Type
import pickle # not in use here?
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
                 "head_title": "Aktuelle korona tall for din.kommune.nu",
                 "updated": updated,
                 "nordate": nordate,
                 "hero_title": "din",
                 "hero_isurl": True,
                 "hero_link": "din.kommune.nu",
                 "hero_subtitle": "Dagsaktuelle tall for ditt hjemsted",
                 "html_lang": lang,
                 "lang_selector": selector,
                 "languages": langs,
                 "menu_selected": 0 # 1 = hjem, 2=sp, 3=om
                 }

    return (s, init_dict)


async def robots_txt(request):
    """ simple robots.txt file """
    return PlainTextResponse("User-agent: * Disallow:")

async def robots_nodebug_txt(request):
    """ simple deny-all robots.txt file """
    return PlainTextResponse("User-agent: * Disallow: /debug_info")

async def norobots_txt(request):
    """ simple deny-all robots.txt file """
    return PlainTextResponse("User-agent: * Disallow: /")


def mini_plot_risk(pro100k:float) -> Type[bytes]:
    """
    Simple "gauge" type graphic, not really a plot.
    Gives an impression of current risk level,
    e.g. orange-close-to-green or close-to-red..
    Returns matplotlib base64 encoded png as bytes
    Note: badly behaved async def, no awaits() ....
    """
    pro100k = float(f"{pro100k:.2f}")
    calc_ylim = round(pro100k)+50
    if calc_ylim < 200: calc_ylim = 200
    fig, ax = plt.subplots()
    ax.margins(0)
    ax.axhspan(0,24.9, facecolor="green", alpha=0.5)
    ax.axhspan(25,149.9, facecolor="orange", alpha=0.50)
    ax.axhspan(150, 600, facecolor="red", alpha=0.5)
    plt.xlim(0, 1)
    plt.ylim(0, calc_ylim)
    plt.xlabel("")
    plt.ylabel("")
    #plt.title(pro100k)
    plt.title("Risiko", fontsize='x-small')
    plt.axhline(
        linewidth=3,
        color="black",
        y=pro100k,
        xmin=0.05,
        xmax=0.95,
        linestyle="solid",
        dash_capstyle="round"
    )
    ax.spines['right'].set_visible(False)
    ax.spines['top'].set_visible(False)
    ax.spines['bottom'].set_visible(False)
    ax.spines['left'].set_position(('outward', 10))
    fig.set_size_inches(2,3)
    plt.tick_params(
        axis='x',
        which='both',
        bottom=False,
        top=False,
        labelbottom=False
    )
    fig.tight_layout()
    img = io.BytesIO()
    plt.savefig(img, format="png")
    img.seek(0)
    plt.close() # Not sure this is needed
    return base64.b64encode(img.read())


def mini_plot_trend(kid:str) -> Type[bytes]:
    """
    Small lineplot to depict 14-day development
    x-axis is date, and y diff cases per 100k
    Returns matplotlib/seaborn base64 encoded png as bytes
    """
    df_kid = pd.DataFrame(korona.app_get_plotdata(kid, 2))
    #df_nor = pd.DataFrame(korona.app_get_plotdata('0000', 2))
    df_kid['diff_kom'] = df_kid["per_100k"].diff()
    #df_kid['diff_nor'] = df_nor["per_100k"].diff()
    del df_kid['per_100k'] # don't need N just diff

    # debug control data
    #print(f"data control: df_kid = {df_kid}")

    fig, ax = plt.subplots(figsize=(6,3))
    sns.lineplot(ax=ax, x="dato", y="diff_kom", data=df_kid, linewidth=5)
    #sns.set_style("whitegrid")
    sns.set_style("white")
    sns.set_context("talk")
    sns.despine(offset=5, trim=True, left=False)

    # Get Norwegian labels for xtics datestamps
    xtic_lab = list(df_kid.to_dict()['dato'].values())
    #use_tic = [ xtic_lab[1], xtic_lab[-1] ] # samme som xtics_nor utgangspunkt


    xtics_nor = [xtic_lab[1], xtic_lab[-1]] # note: on purpose, [0] is NaN
    xtics_nor.reverse()
    xtic_lab.reverse()
    xtics_nor = [ korona.norwegian_date(x, True) for x in xtics_nor ]
    xtics_nor = [ x.replace(" 2020","").replace(" 2021","") for x in xtics_nor ]
    ax.set_xticks([xtic_lab[0], xtic_lab[-2]])


    #print(f"xtics_nor: {xtics_nor}")
    #print(f"xtics_lab: {xtic_lab}")
    #print(f"lab slice: {xtic_lab[1]},{xtic_lab[-1]}")
    #print(f"use_tic: {use_tic}")

    ax.set_xticklabels([xtics_nor[0], xtics_nor[1]])

    plt.yticks()
    plt.tick_params(axis='x', which='both', bottom=True, top=False, labelbottom=True)
    plt.ylabel('')
    plt.xlabel('')
    plt.title("Tilfeller per 100K per dag", fontsize='x-small')
    fig.tight_layout()
    img = io.BytesIO()
    plt.savefig(img, format="png")
    img.seek(0)
    plt.close() # Not sure this is needed
    return base64.b64encode(img.read())


async def debug_output_state(request):
    """ Simple debug output for korona.py """
    s, response_dat = get_template_vars() # Get session
    data, _ = korona.app_query('5401')
    response_dat.update(
        {
        "s": dir(s),
        "data": data
        }
    )
    print(response_dat.items()) # debug in cli
    long_string = ""
    for k,v in data.items():
        long_string += f"{k}={v} \n"
    return PlainTextResponse(print(long_string))

async def subdomain_vvhf(request):
    """
    Vestre Viken HF subdomene
    Relies on selections from custom_queries attr in Session object
    """

    # push css (http2/http3)
    await request.send_push_promise("/css/bulma.min.css")

    if request.method == "POST":
        return PlainTextResponse("post to VVHF")
    else:
        s, response_dat = get_template_vars() # Get session
        try:
            _ = s.vvhf_keys
        except:
            s.vvhf_keys = [ "vvhf", "bersyk", "dramsyk", "kongsyk", "ringsyk"]

        try:
            _ = s.vvhf_sites
        except:
            s.vvhf_sites = {}
            for key in s.vvhf_keys:
                s.vvhf_sites[key] = {
                    "title": s.custom_queries[key]['title'],
                    "subtitle": s.custom_queries[key]['subtitle'],
                    "created": s.custom_queries[key]['created'],
                    "list":  s.custom_queries[key]['list'],
                    "url": key
                    }


        # Get request data
        try:
            # Get query param from template/URL
            fetching = request.query_params['vis']
        except:
            # or go to default landing page
            fetching = "vvhf"

        # Just make sure
        if fetching not in s.vvhf_keys: fetching = "vvhf"

        # Update fields
        page_title = s.custom_queries[fetching]['title']
        page_subtitle = s.custom_queries[fetching]['subtitle']

        items, _ = korona.app_get_items(
            s.custom_queries[fetching]['list']
            )
        data, _ = korona.app_query(items)

        # Sort by cases per 100k # TODO simplify this
        # Can prolly do this with a quick lambda
        # print("debug")
        # print(f"data = {data}")

        by_risk = {}
        for item in data.keys():
            if item == '0000': continue
            score = data[item]['diff_100k'][0]
            by_risk.update({item: score})

        data_ordering = sorted(by_risk, key=by_risk.get, reverse=True)
        data_sorted = {}
        for item in data_ordering:
            data_sorted[item] = data[item]


        response_dat.update(
            {
            "request": request,
            "head_title": "Gjeldende korona-tall for VVHF kommuner",
            "hero_title": page_title,
            "hero_isurl": False,
            "hero_subtitle": page_subtitle,
            "hero_link": "vvhf.kommune.nu",
            "vvhf_sites": s.vvhf_sites,
            "result_dict": data_sorted,
            "current": fetching
            }
        )
        return templates.TemplateResponse('vvhf.t', response_dat)


async def find_muncipality_in(req: str) -> str:
    """
    Test GET string for actionable requests
    """
    s, _ = get_template_vars()

    # # DEBUG:
    #print("inside find_muncipality_in()")

    # check string against norway data
    fetch_id = s.norge.id_from_url.get(req, None)

    # if no hits, traverse options
    if fetch_id is None:
        input_category = req.split(sep="-")
        if len(input_category) == 1:
            return req
        elif "-fylke" in req:
            return req
        else:
            # two or more words: conjunctive or name containing dash
            if len(input_category) > 2:
                a, b, *c = req.split(sep="-")
                return f"{a.capitalize()} og {c[0].capitalize()}"
            else:
                a, *b = req.split(sep="-")
                return f"{a.capitalize()}-{b[0].capitalize()}"
    else:
        return fetch_id


async def subdomain_parser(request):
    """
    Internal route for different subdomains
    This is the main entry point for requests that are not
    to "main_site" subdomains (e.g. www, din, korona etc.)
    """
    #await request.form()
    #print("in subdomain_parser")
    # Get korona.Session object "s"
    s, response_dat = get_template_vars()

    # push css (http2/http3)
    await request.send_push_promise("/css/bulma.min.css")

    # grab string from subdomain
    full_url = str(request.url)
    subdomain = full_url.split(sep="//")[1].split(sep=".")[0].lower()

    # # check string against norway data
    # fetch_id = s.norge.id_from_url.get(subdomain, None)
    #
    # # if no hits, traverse options
    # if fetch_id is None:
    #     input_category = subdomain.split(sep="-")
    #     if len(input_category) == 1:
    #         fetch_item = subdomain
    #     elif "-fylke" in subdomain:
    #         fetch_item = subdomain
    #     else:
    #         # two or more words: conjunctive or name containing dash
    #         if len(input_category) > 2:
    #             a, b, *c = subdomain.split(sep="-")
    #             fetch_item = f"{a.capitalize()} og {c[0].capitalize()}"
    #         else:
    #             a, *b = subdomain.split(sep="-")
    #             fetch_item = f"{a.capitalize()}-{b[0].capitalize()}"
    # else:
    #     fetch_item = fetch_id

    fetch_item = await find_muncipality_in(subdomain)

    # Get the deets
    items, item_type = korona.app_get_items([fetch_item])


    if len(items) == 1:
        if item_type == 0:
            # Get the url-friendly string
            return subdomain_kommune(items[0], request)
            #await subdomain_kommune(items[0], request)
        elif subdomain == "oslo-fylke" or subdomain == "oslo": # override
            return subdomain_kommune(items[0], request)
            #await subdomain_kommune(items[0], request)
        else:
            search_url = "https://sjekk.kommune.nu/?s"
            return RedirectResponse(url=f'{search_url}={items[0]}')
    elif item_type == 1:
        return subdomain_fylke(items, subdomain, request) # ???
    else:
        search_url = "https://sjekk.kommune.nu/"
        return RedirectResponse(url=f"{search_url}")



def subdomain_fylke(flist:list, fname:str, request):
    """
    Shows only_one table template for requested county
    """

    # query input list "flist"
    data, skipped_items = korona.app_query(flist)
    _kingdom = data.pop('0000')

    # get category count
    # legend data['4224']['risk'] = 0|1|2 (3=NA)
    green_orange_red = [0, 0, 0, 0]
    for m in data.keys():
        green_orange_red[data[m]['risk']] += 1


    # get session and response dict
    s, response_dat = get_template_vars()

    # Lookup fylke name from subdomain
    fylke_names = s.norge.fylke_url_name

    # get web template strings
    subdomain = fname
    fylke = fylke_names[fname]
    fylke_alt = None
    if fylke in s.norge.alt_name.keys():
        fylke_alt = s.norge.alt_name[fylke]

    # set default title/subtitle
    hero_title = f"Aktuelle tall for {fylke}"
    hero_link = f"{subdomain}.kommune.nu"
    hero_subtitle = hero_link
    if fylke_alt:
        hero_subtitle = fylke_alt

    # pick right template type
    if len(flist) == 1:
        only_one, exactly_two = True, False
    elif len(flist) == 2:
        only_one, exactly_two = False, True
    else:
        only_one, exactly_two = False, False

    # update response dict
    response_dat.update(
                    {
                    "request": request,
                    "head_title": f"Korona-tall for {fylke}",
                    "hero_title": hero_title,
                    "hero_isurl": False,
                    "hero_link": hero_link,
                    "hero_subtitle": hero_subtitle,
                    "skipped_items": skipped_items,
                    "result_dict": data,
                    "green_orange_red": green_orange_red,
                    "only_one": only_one,
                    "exactly_two": exactly_two
                    }
    )

    return templates.TemplateResponse('table.t', response_dat)


async def subdomain_endpoint(template:str, response_dat:dict):
    return templates.TemplateResponse(template, response_dat)


def subdomain_kommune(kid:str, request):
    """
    Shows only_one table template for requested muncipality
    For full commentary see fritekst()
    """
    s, response_dat = get_template_vars()

    # Get results data
    data, skipped_items = korona.app_query([kid])
    mini_dict = data[list(data.keys())[0]]
    _kingdom = data.pop('0000')

    # Get plot data dictionary
    # Fetches base64 encoded bytestring of plot images
    diff_pro100k = data[kid]['diff_100k'][0] # reelvant for risk
    trend_plot = mini_plot_trend(kid)
    level_plot = mini_plot_risk(diff_pro100k)

    # Set strings
    hero_title = mini_dict['name']
    head_title = f"Korona-status for {hero_title}"
    hero_link = mini_dict['url']
    subtitle = mini_dict['alt']
    hero_subtitle = "Tall for din kommune"
    if subtitle:
        hero_subtitle = mini_dict['alt']
    response_dat['hero_link'] = hero_link

    # Build response dict
    response_dat.update(
                    {
                    "request": request,
                    "head_title": head_title,
                    "hero_title": hero_title,
                    "hero_isurl": False,
                    "hero_link": hero_link,
                    "hero_subtitle": hero_subtitle,
                    "skipped_items": skipped_items,
                    "result_dict": data,
                    "trend_plot": trend_plot.decode('utf-8'),
                    "level_plot": level_plot.decode('utf-8'),
                    "only_one": True,
                    "exactly_two": False,
                    "green_orange_red": []
                    }
    )

    #test_weird = templates.TemplateResponse('table.t', response_dat)
    #return test_weird
    #return await subdomain_endpoint('table.t', response_dat)
    return templates.TemplateResponse('table.t', response_dat)



async def hjem(request):
    # fetch minimal data
    s, response_dat = get_template_vars()
    today = s.datapoints[0]

    await request.send_push_promise("/css/bulma.min.css")

    # check subdomain
    # full_url = str(request.url)
    # subdomain = full_url.split(sep="//")[1].split(sep=".")[0].lower()
    # if subdomain in ["korona", "din", "om", "www"]:
    #     if subdomain == "om":
    #         response = RedirectResponse(url='/om')
    #     elif subdomain == "sjekk":
    #         response = RedirectResponse(url='/utvalg')
    # else:
    #     items, item_type = korona.app_get_items([subdomain])
    #     if len(items) == 1:
    #         if item_type == 0:
    #             await subdomain_kommune(items[0], request)
    #         elif item_type == 1:
    #             return RedirectResponse(url=f'/f/{items[0]}')
    #         else:
    #             search_url = "https://sjekk.kommune.nu/?sok"
    #             return RedirectResponse(url=f"{search_url}={items[0]}")

    try:
        # Get data from today
        response_dat.update(s.book['ro']['0000'][today])
    except KeyError:

        # We can't not show anything, fallback to yesterday's data
        for datapoint in s.datapoints:
            try:
                data_test = s.book['ro']['0000'][datapoint]
            except KeyError:
                data_test = None

            if data_test is None:
                today = None
            else:
                today = datapoint

        if today is None:
            response_dat.update(
                    {
                    'diff_n': 'NA', # number of new infected people last 24 hrs
                    'infected': 'NA', # muncipalities with infected (bool)
                    'orange': 'NA',
                    'green': 'NA', # muncipalities
                    'red': 'NA'
                   }
            )
        else:
            updated = today
            nordate = today
            if user_lang.active == "norsk":
                nordate = korona.norwegian_date(today, True)

            response_dat.update(s.book['ro']['0000'][today])

    # construct rest of index vars
    response_dat.update(
        {
            "request": request,
            "menu_selected": 1 # 1 = hjem, 2=sp, 3=om
        }
    )

    # Return index template with vars
    return templates.TemplateResponse('index.t', response_dat)


async def search_parser(request):
    """ GET/POST conditional for sjekk.kommune.nu subdomain"""
    await request.form()
    if request.method == "POST":
        return PlainTextResponse(f"{data}")
    else:
        try:
            # See if we're searching
            _ = html.escape(request.query_params['s'])
            return fritekst(request)
        except:
            # Not searching, display regular utvalg page
            s, response_dat = get_template_vars()
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

            response_dat.update(
                {
                    "request": request,
                    "head_title": "sjekk.kommune.nu korona spørring",
                    "hero_title": "sjekk",
                    "hero_isurl": True,
                    "hero_subtitle": "Velg hvilke kommuner du vil se",
                    "hero_link": "sjekk.kommune.nu/utvalg",
                    "fylker": big_list,
                    "utvalg": 0,
                    "menu_selected": 2 # 1 = hjem, 2=sp, 3=om
                }
            )
    return templates.TemplateResponse('utvalg.t', response_dat)


def fritekst(request):
    #await request.form()
    try:
#        print("debug")
#        print(request.query_params.keys())
        ui = html.escape(request.query_params['s'])

        # /?sok=Salangen

    except Exception as e:
        # could not get input ..? => bail!
        print(f"got exception: {e}")
        return RedirectResponse(url='https://din.kommune.nu') # TBD 404


    ui = ui.replace("!","").replace("\\","").replace("/","")
    uinput = ui

    # create response dict for template
    s, response_dat = get_template_vars()
    #print(f"current = '{uinput}'")
    sammenslaatt = s.norge.sammenslaatt()

    if uinput.lower() in sammenslaatt:
        uinput = uinput.split(sep=",")
    else:
        # tillatt folk å bruke "og"
        print(f"current init = '{uinput}'")
        uinput = uinput.replace(" ",",").replace("og","").replace(",,",",")
        uinput = [ y for x in uinput.split(sep=",") for y in x.split(sep=",og,")]

    print(f"current = '{uinput}'")


    # THIS FAILS: Kunne ikke finne: <['Oslo og Bergen']>
    #

    # Nota bene, enkelte søk fungerer ikke:
    # Oslo, Bergen, og Lavangen gir ...?
    # Oslo, Bergen og Lavangen gir Lavangen
    # Oslo og Bergen og Lavangen
    # Oslo og Lavangen, Bergen
    # Oslo,Bergen,Lavangen

    # Redirect customs here
    if uinput[0] in s.custom_queries.keys():
        if uinput[0] == "vvhf":
            return RedirectResponse(url='https://vvhf.kommune.nu')

    # Check that we have input
    items_to_display, query_type = korona.app_get_items(uinput)

    print(f"debug to_fetch={items_to_display}")
    print(f"query_type={query_type}")

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
        hero_link = head_title
        hero_title = "sjekk"
        hero_isurl = True
        hero_subtitle = "Aktulle tall for ditt søk"

        # Quickie
        short_dict = data[list(data.keys())[0]]

        if only_one:
            item_name = short_dict['name']
            if query_type == 0:
                # kommune
                item_url = short_dict['url']
                return RedirectResponse(url=f"https://{item_url}")
            elif query_type == 1:
                try:
                    fylke_url = short_dict['fylke-url']
                except:
                    fylke_url = s.norge.get_fylke_url(item_name)
                return RedirectResponse(url=f"https://{fylke_url}")

            hero_title = item_name
            hero_isurl = False
            head_title = f"Korona-status for {item_name}"
#            hero_title = data[list(data.keys())[0]]['url']
            hero_link = short_dict['url']
            subtitle = short_dict['alt']
            hero_subtitle = "Tall for din kommune "
            if subtitle:
                hero_subtitle = short_dict['alt']
            response_dat.update({ "hero_link": hero_link })
        elif exactly_two:
            kom_1 = short_dict['name']
            kom_2 = data[list(data.keys())[1]]['name']
            hero_subtitle = f"{kom_1} og {kom_2}"
            head_title = f"Korona-status for {kom_1} og {kom_2}"
        else:
            n_of_n = f"{returned_items}/{len(items_to_display)}"
            nordate = response_dat['nordate']
            hero_subtitle = f"Viser {n_of_n} treff fra oppslag (data fra {nordate})"

        # make a custom hero for fylker
        # if query_type == 1:
        #     q = uinput[0].capitalize()
        #     if " og " in q:
        #         a, b = uinput[0].split(sep=" og ")
        #         q = f"{a.capitalize()} og {b.capitalize()}"
        #
        #     #print(f"q in {q}")
        #     if q in s.norge.fylker.keys():
        #         hero_title = f"Aktuelle tall for {q}"
        #     else:
        #         fylke = None
        #         for k, v in s.norge.alt_name.items():
        #             for subkey in v.split(sep=" - "):
        #                 if q.lower() in subkey.lower():
        #                     hero_subtitle = v
        #                     hero_title = f"Aktuelle tall for {k}"

        # custom hero for custom queries
        if query_type == 2:
            hero_isurl = False
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
                        "hero_isurl": hero_isurl,
                        "hero_link": hero_link,
                        "hero_subtitle": hero_subtitle,
                        "skipped_items": skipped_items,
                        "result_dict": data,
                        "only_one": only_one,
                        "exactly_two": exactly_two,
                        "menu_selected": 2, # 1 = hjem, 2=sp, 3=om
                        "green_orange_red": []
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

    await request.send_push_promise("/css/bulma.min.css")

    subtitle = "Kjapp oversikt med tall fra FHI"
    s, response_dat = get_template_vars()
    response_dat.update(
        {
            "request": request,
            "head_title": "Om kommune.nu",
            "hero_link": "din.kommune.nu/om",
            "hero_title": "Om kommune.nu",
            "hero_isurl": False,
            "hero_subtitle": subtitle,
            "menu_selected": 3 # 1 = hjem, 2=sp, 3=om
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
                "head_title": "sjekk.kommune.nu korona spørring",
                "hero_title": "sjekk",
                "hero_isurl": True,
                "hero_subtitle": "Velg hvilke kommuner du vil se",
                "hero_link": "sjekk.kommune.nu/utvalg",
                "fylker": big_list,
                "utvalg": 0,
                "menu_selected": 2 # 1 = hjem, 2=sp, 3=om
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
                "head_title": "sjekk.kommune.nu korona spørring",
                "hero_title": "sjekk",
                "hero_isurl": True,
                "hero_subtitle": "Velg hvilke fylker du vil sjekke",
                "hero_link": "sjekk.kommune.nu/fylker",
                "fylker": big_list,
                "menu_selected": 2, # 1 = hjem, 2=sp, 3=om
                "utvalg": 1
            }
        )
        return templates.TemplateResponse('utvalg.t', response_dat)

async def utvalg_hjelp(request):
    # get language settings
    s, response_dat = get_template_vars()
    response_dat.update(
        {
            "request": request,
            "head_title": "korona.kommune.nu spørring",
            "hero_title": "sjekk",
            "hero_isurl": True,
            "hero_subtitle": "Hjelp til spørring",
            "hero_link": "sjekk.kommune.nu/hjelp",
            "menu_selected": 2, # 1 = hjem, 2=sp, 3=om
            "utvalg": 3
        }
    )
    return templates.TemplateResponse('utvalg.t', response_dat)

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

    response_dat.update(
        {
            "request": request,
            "head_title": "korona.kommune.nu spørring",
            "hero_title": "sjekk",
            "hero_isurl": True,
            "hero_subtitle": "Egendefinerte spørringer",
            "hero_link": "sjekk.kommune.nu/egen",
            "fylker": big_list,
            "menu_selected": 2, # 1 = hjem, 2=sp, 3=om
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


async def kom_fylk(request):
    """ Deals with legacy /k or /f requests """
    try:
        key = list(request.path_params.values())[0]
    except:
        re_url = "hjelp"
    else:
        re_url = f"?s={key}"
    finally:
        url = "https://sjekk.kommune.nu"
        return RedirectResponse(url=f"{url}/{re_url}")

#@app.routes('/testing', methods=['POST'])
#async def ipn_post(request):
#    print('hi')
 #   print(request.form())

#async def confirmation(request):
#    return templates.TemplateResponse('confirmation.html', {'request': request})

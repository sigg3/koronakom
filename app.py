#!/usr/bin/env python3
# coding=utf-8
from starlette.applications import Starlette

from starlette.middleware import Middleware
from starlette.middleware.trustedhost import TrustedHostMiddleware
from starlette.middleware.httpsredirect import HTTPSRedirectMiddleware
#from starlette.endpoints import HTTPEndpoint
#from starlette.responses import PlainTextResponse
#from starlette.requests import Request
#from starlette.responses import Response
from starlette.routing import Route, Mount, Host, Router
from starlette.staticfiles import StaticFiles
import multipart
#from starlette.templating import Jinja2Templates
from routes import *
import korona
#import datetime

#templates = Jinja2Templates(directory='templates')

# class Hjem(HTTPEndpoint):
#     async def get(self, request):
#         html_languages = [ "Norsk", "Engelsk", "Ditt språk" ]
#         sist_oppdatert = datetime.datetime.now().isoformat().split(sep="T")[0]
#         return templates.TemplateResponse('index.html', {'request': request, 'updated': sist_oppdatert, 'html_lang': html_languages})
#
#     async def post(self, request):
#         print(request.form())
#         return PlainTextResponse(f"success: request.form = {request.form()}")
#
#
# #Route('/users/{user_id:int}', user, methods=["GET", "POST"])
#
#
# class Fylke(HTTPEndpoint):
#     async def get(self, request):
#         print(dir(request))
#         print(f"url = {request.url}")
#         f_name = request.path_params['f']
#         return PlainTextResponse(f"This is fylke = {f_name}")
#
# class Kommune(HTTPEndpoint):
#     async def get(self, request):
#         perma = request.path_params['id']
#         #return Kommune
#         return PlainTextResponse(f"Navigate to {perma}")
#

# Startup task
async def initialize_korona():
    """
    Will run setup() equivalent to main() to download
    and build current database from sources, and save
    to binary pickle file in Settings.store attribute
    """
    await korona.setup()
    print("initialization complete")


async def clean_up_korona():
    """
    Sift through pickle file and remove outdated items
    (runs korona.clear_data())
    """
    pass


# Middleware
# Note: let us do HTTPSRedirectMiddleware when TLS available
middleware = [
    Middleware(
        TrustedHostMiddleware, allowed_hosts=['kommune.nu',
                                              '*.kommune.nu'
#                                              'localhost',
#                                              '*.localhost'
                                              ]
            ),
    Middleware(HTTPSRedirectMiddleware)
]



#subdomain_app = Router(
#    routes=[Host("{subdomain}.example.org", app=subdomain_app, name="subdomains")]
#)



#
# test_router = Router(
#     routes = [Host('www.{global_domain}', app=subdomain_app)]
#             routes=[Route("/", RedirectResponse('din.localhost'))]
#         ),
#         Host(
#             'korona.{global_domain}',
#             routes=[Route("/", RedirectResponse('din.localhost'))]
#         ),
#         Host(
#             'din.{global_domain}',
#             routes=[
#                  Route('/', hjem, name="homepage"),
#                  Route('/sok/{sok:path}', fritekst),
#                  Route('/lang/{set_lang}', endre_spraak),
#                  Route('/utvalg', utvalg),
#                  Route('/fylker', utvalg_fylker, methods=["GET", "POST"]),
#                  Route('/egen', utvalg_egen),
#                  Route('/om', om_tjenesten),
#                  Route('/f/{fylke}', fylke),
#                  Route('/k/{kom}', kommune),
#                  Mount('/css', StaticFiles(directory="static"), name="css")
#                  ]
#              ),
#         Host(
#             '{subdomain}.{global_domain}',
#             routes = [
#                  Route('/', subdomain_kommune),
#                  Mount('/css', StaticFiles(directory="static"), name="css")
#                  ]
#              )
#         ]
# )


# Application
app = Starlette(
                debug=True, # set to false in production
                middleware=middleware,
                on_startup=[initialize_korona],
                on_shutdown=[clean_up_korona]
)



# TODO
#din.kommune.nu/utvalg
#din.kommune.nu/fylker
#din.kommune.nu/egen
#sjekk.kommune.nu/ -> fritekst





# Routing
site_main = Router(
     routes=[
        Route('/', hjem, name="homepage"),
#        Route('/sok/{sok:path}', fritekst),
        Route('/lang/{set_lang}', endre_spraak),
#        Route('/utvalg', utvalg), # TODO remove
#        Route('/hjelp', utvalg_hjelp), # TODO remove
#        Route('/fylker', utvalg_fylker, methods=["GET", "POST"]), # TODO remove
#        Route('/egen', utvalg_egen), # TODO remove
        Route('/om', om_tjenesten),
        Route('/f/{fylke}', fylke), # TODO remove
        Route('/k/{kom}', kommune), # TODO remove
        Mount('/css', StaticFiles(directory="static"), name="css")
        ]
)

site_search = Router(
    routes=[
#        Route('/', utvalg_hjelp, methods=["GET"]),
#        Route('/{s:path}', fritekst, methods=["POST"])),
        Route('/', search_parser, methods=["GET", "POST"]),
        Route('/hjelp', utvalg_hjelp),
        Route('/utvalg', utvalg, methods=["GET", "POST"]),
        Route('/fylker', utvalg_fylker, methods=["GET", "POST"]),
        Route('/egen', utvalg_egen),
        Mount('/css', StaticFiles(directory="static"), name="css")
        ]
)

site_subdomains = Router(
    routes=[
        Route('/', subdomain_parser, name="sub"),
        Mount('/css', StaticFiles(directory="static"), name="css")
        ]
)

site_vvhf = Router(
    routes=[
        Route('/', subdomain_vvhf),
        Mount('/css', StaticFiles(directory="static"), name="css")
        ]
)

# TODO om, utvalg, sjekk etc. kontakt?

# Main page aliases
app.host('www.kommune.nu', site_main)
app.host('din.kommune.nu', site_main)
app.host('min.kommune.nu', site_main)
app.host('korona.kommune.nu', site_main)

# Domain specific subdomains
app.host('sjekk.kommune.nu', site_search)
app.host('vvhf.kommune.nu', site_vvhf)

# Wildcard (either muncipality or county)
app.host('{subdomain}.kommune.nu', site_subdomains)

#app.host('www.localhost', site_main)
#app.host('din.localhost', site_main)
#app.host('korona.localhost', site_main)
#app.host('sjekk.localhost', site_search)
#app.host('vvhf.localhost', site_vvhf)
#app.host('{subdomain}.localhost', site_subdomains)

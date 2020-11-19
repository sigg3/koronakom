#!/usr/bin/env python3
# coding=utf-8
from starlette.applications import Starlette

from starlette.middleware import Middleware
from starlette.middleware.trustedhost import TrustedHostMiddleware

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
    korona.setup()


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
        TrustedHostMiddleware, allowed_hosts=[
                                              'kommune.nu',
                                              '*.kommune.nu',
                                              'localhost',
                                              '*.localhost'
                                              ]
            )
        ]

# subdomain example
# app = Starlette()
# site = Router()  # Use eg. `@site.route()` to configure this.
# subdomains = Router()  # Use eg. `@subdomains.route()` to configure this.
# app.host('www.example.org', site)
# app.host('{subdomain}.example.org', kommune_url)
# kommune_url = Router()

app = Starlette(debug=True, routes=[
#  Route('/', hjem, methods=["POST"]),
  Route('/', hjem, name="homepage"),
#  Route('/sjekk/{input:str}', sjekk, methods=["GET"]),
#  Route('/{input:str}', sjekk, methods=["GET"], subdomain="sjekk"),
  #Route('/?sok={input:str}', sjekk_input, methods=["GET"]),
 # Route('/sok', sjekk_input, methods=["GET"]),
  Route('/sok/{sok:path}', fritekst),
#  Route('/users/{user_id:int}', user, methods=["GET", "POST"]),
  Route('/lang/{set_lang}', endre_spraak),
  Route('/utvalg', utvalg),
  Route('/fylker', utvalg_fylker, methods=["GET", "POST"]),
  Route('/egen', utvalg_egen),
  Route('/om', om_tjenesten),
#  Route('/vvhf', vestre_viken),
  Route('/f/{fylke}', fylke),
  Route('/k/{kom}', kommune),
  #Route('/sjekk', Sjekk),
 # Route('/lang', EndreSpraak)
  Mount('/css', StaticFiles(directory="static"), name="css"),
  # Host(
  #       "ringerike.localhost",
  #       app=Router(routes=[Route("/sok/vvhf", endpoint=custom_subdomain)]),
  #       ),
], middleware=middleware, on_startup=[initialize_korona], on_shutdown=[clean_up_korona])

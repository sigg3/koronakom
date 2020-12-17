{% extends "base.template" %}


<!-- remove this entire block when finished -->
{% block tweety %}
{% if utvalg == 3 %}
<div class="block">&nbsp;</div>
{% else %}
<div class="tile is-ancestor">
    <div class="tile is-4">&nbsp;</div>
    <div class="tile is-4">
        <div class="notification is-warning">
          <strong>Beklager!</strong>
          Denne delen av siden er dessverre ikke ferdig utviklet.
          Det kan hende noe fungerer og andre ting ikke gjør det.
          Lykke til :)
        </div>
    </div>
    <div class="tile is-4">&nbsp;</div>
</div>

<div class="block">&nbsp;</div>
{% endif %}
{% endblock %}



{% block sector_1 %}
<div class="tile is-ancestor pb-4">
    <div class="tile is-4">
        &nbsp;
    </div>
    <div class="tile is-4">
        <div class="container has-text-centered pl-1 pr-1">
            <div class="level has-text-centered is-mobile">
                {% if utvalg == 0 %}
                <p class="level-item"><a href="https://sjekk.kommune.nu/" title="Hjelp til s&oslash;k" class="button is-light">S&oslash;k</a></p>
                <p class="level-item"><a href="https://sjekk.kommune.nu/utvalg" title="Velk kommuner enkeltvis" class="button is-info"><strong>Kommune</strong></a></p>
                <p class="level-item"><a href="https://sjekk.kommune.nu/fylker" title="Velg etter fylke" class="button is-light">Fylke</a></p>
                <p class="level-item"><a href="https://sjekk.kommune.nu/egen" title="Egendefinert utvalg" class="button is-light">Egen</a></p>
                {% elif utvalg == 1 %}
                <p class="level-item"><a href="https://sjekk.kommune.nu/" title="Hjelp til s&oslash;k" class="button is-light">S&oslash;k</a></p>
                <p class="level-item"><a href="https://sjekk.kommune.nu/utvalg" title="Velk kommuner enkeltvis" class="button is-light">Kommune</a></p>
                <p class="level-item"><a href="https://sjekk.kommune.nu/fylker" title="Velg etter fylke" class="button is-info"><strong>Fylke</strong></a></p>
                <p class="level-item"><a href="https://sjekk.kommune.nu/egen" title="Egendefinert utvalg" class="button is-light">Egen</a></p>
                {% elif utvalg == 2 %}
                <p class="level-item"><a href="https://sjekk.kommune.nu/" title="Hjelp til s&oslash;k" class="button is-light">S&oslash;k</a></p>
                <p class="level-item"><a href="https://sjekk.kommune.nu/utvalg" title="Velk kommuner enkeltvis" class="button is-light">Kommune</a></p>
                <p class="level-item"><a href="https://sjekk.kommune.nu/fylker" title="Velg etter fylke" class="button is-light">Fylke</a></p>
                <p class="level-item"><a href="https://sjekk.kommune.nu/egen" title="Egendefinert utvalg" class="button is-info"><strong>Egen</strong></a></p>
                {% else %}
                <p class="level-item"><a href="https://sjekk.kommune.nu/" title="HHjelp til s&oslash;k" class="button is-info"><strong>S&oslash;k</strong></a></p>
                <p class="level-item"><a href="https://sjekk.kommune.nu/utvalg" title="Velk kommuner enkeltvis" class="button is-light">Kommune</a></p>
                <p class="level-item"><a href="https://sjekk.kommune.nu/fylker" title="Velg etter fylke" class="button is-light">Fylke</a></p>
                <p class="level-item"><a href="https://sjekk.kommune.nu/egen" title="Egendefinert utvalg" class="button is-light">Egen</a></p>
                {% endif %}
            </div>
        </div>
    </div>
    <div class="tile is-4">
        &nbsp;
    </div>
</div>
{% endblock %}

{% block sector_2 %}
{% if utvalg < 2 %}
<form action="https://sjekk.kommune.nu/" method="POST">
{% endif %}
<div class="tile is-ancestor mt-2">
    {% if utvalg == 0 %}
    <div class="tile is-3">&nbsp;</div>
    <div class="tile is-8">
    {% else %}
    <div class="tile is-4">&nbsp;</div>
    <div class="tile is-4">
    {% endif %}
        <div class="container ml-2 mr-2 pl-2 pr-2">
            {% if utvalg == 0 %}
                {% for f, k in fylker.items() %}
                <h1 class="title">{{ f }}</h3>
                {% if f != "Oslo" %}
                    <div class="control">
                        <h2 class="subtitle">
                            Vis alle i {{ f }} fylke:
                            <label class="radio">
                                <input type="radio" value="1" name="{{ f }}"> Ja
                            </label>
                            <label class="radio">
                                <input type="radio" value="0" name="{{ f }}" checked> Nei
                            </label>
                            <span class="has-text-grey-light">(overstyrer)</span>
                        </h2>
                    </div>
                <div class="block">&nbsp;</div>
                {% endif %}
                {% for kommune in k %}
                <label class="checkbox" style="width: 14em;">
                    <input type="checkbox" value="1" name="{{ kommune[1] }}">
                    <a href="https://{{ kommune[2] }}" title="{{ kommune[0] }}">{{ kommune[0] }}</a>
                </label>
                {% endfor %}
                <div class="block">&nbsp;</div>
                {% endfor %}
                <h1 class="title">Tilpasninger</h1>
                <div class="control">
                    <h2 class="subtitle">
                        Vis i rekkefølge:
                        <label class="radio" checked>
                            <input type="radio" value="0" name="sort_results" checked> utvalg
                        </label>
                        <label class="radio">
                            <input type="radio" value="1" name="sort_results"> synkende (høy-lav)
                        </label>
                        <label class="radio">
                            <input type="radio" value="2" name="sort_results"> stigende (lav-høy)
                        </label>
                    </h2>
                    <h2 class="subtitle">
                        Visningstype (for &gt;2):
                        <label class="radio" checked>
                            <input type="radio" value="1" name="list_results" checked> liste
                        </label>
                        <label class="radio">
                            <input type="radio" value="0" name="list_results"> tabell
                        </label>
                    </h2>
                </div>
            {% elif utvalg == 1 %}
            <div class="container has-text-centered">
                <h2 class="subtitle">La meg se p&aring;:</h2>
                     <div class="control has-text-left ml-6 ">

                    {% for f, k in fylker.items() %}
                    <label class="checkbox" style="display: block;">
                        <input type="checkbox" name="{{ f }}">
                        <a href="https://sjekk.kommune.nu/?s={{ f }}" title="{{ f }}">{{ f }}</a>
                    </label>
                    {% endfor %}
                    </div>
                <h2 class="subtitle">Tilpasninger</h1>
                <div class="control">
                    <p>Vis i rekkefølge:
                        <label class="radio" checked>
                            <input type="radio" value="0" name="sort_results" checked> utvalg
                        </label>
                        <label class="radio">
                            <input type="radio" value="1" name="sort_results"> synkende (høy-lav)
                        </label>
                        <label class="radio">
                            <input type="radio" value="2" name="sort_results"> stigende (lav-høy)
                        </label>
                    </p>
                    <p>
                        Visningstype (for &gt;2):
                        <label class="radio" checked>
                            <input type="radio" value="1" name="list_results" checked> liste
                        </label>
                        <label class="radio">
                            <input type="radio" value="0" name="list_results"> tabell
                        </label>
                    </p>
                </div>
            </div>
            {% elif utvalg == 2 %}
                <h2 class="subtitle">Egendefinerte sp&oslash;rringer</h2>
                <p>Alle kommunene i Norge har en fire-sifret kode (f.eks. har Oslo 0301).</p>
                <p>&nbsp;</p>
                <p>Denne siden er ikke ferdig utviklet.</p>
                <p>&nbsp;</p>
                <p>Legg inn spørring for EU-risk-assessment</p>
            {% else %}
                <div class="columns is-centered is-hidden-mobile"><!-- desktop  -->
                    <form action="https://sjekk.kommune.nu/" method="get">
                        <div class="field has-addons pt-3">
                            <p class="control is-hidden-mobile"><!-- desktop -->
                                <input name="s" class="input is-large" type="text" placeholder="Kommune, fylke eller nøkkel*">
                            </p>
                            <p class="control is-hidden-mobile">
                                <button type="submit" class="button is-large is-primary">S&oslash;k</button>
                            </p>
                        </div>
                    </form>
                </div>
                <div class="columns is-centered is-hidden-tablet"><!-- mobile  -->
                    <form action="https://sjekk.kommune.nu/" method="get">
                        <div class="field ml-4 has-addons pt-3">
                            <p class="control is-hidden-tablet"><!-- mobile -->
                                <input name="s" class="input" type="text" size="25" placeholder="Kommune, fylke eller nøkkel*">
                            </p>
                            <p class="control is-hidden-tablet">
                                <button type="submit" class="button is-primary">S&oslash;k</button>
                            </p>
                        </div>
                    </form>
                </div>
                <div class="content">
                    <ul>
                        <li>navn på kommune (enkelt-oppslag)</li>
                        <li>&quot;Tana og T&oslash;nsberg&quot; (sammenligning)</li>
                        <li>&quot;Osen, Oslo, Oster&oslash;y&quot; (liste)</li>
                        <li>firesifret kommunenummer, <wbr>e.g. 0301 for Oslo</li>
                        <li>N + firesifret postnummer, e.g. postnummer <wbr>N3401 (Lier) og N3411 (Sylling) går til Lier (primær kommune)</li>
                        <li>navn på fylke (gir liste over kommunene)</li>
                    </ul>
                </div>
                <p>Altarnativer:</p>
                <div class="content">
                    <ul>
                        <li>Man kan bruke <a href="https://sjekk.kommune.nu/utvalg" title="Utvalg">Kommune-velgeren</a> til å gjøre større utvalg manuelt.</li>
                        <li>Det er også lagt inn samme mulighet for fylker i <a href="https://sjekk.kommune.nu/fylker" title="Fylker">fylke-velgeren</a>.</li>
                        <li>Det er i tillegg mulig å få lagt inn egendefinerte spørringer, les mer om det på <a href="https://sjekk.kommune.nu/egen" title="Egendefinerte søk">egendefinerte søk</a>.</li>
                    </ul>
                </div>
            {% endif %}

        </div>
    </div>
    <div class="tile is-1">
        &nbsp;
    </div>
</div>
{% if utvalg < 2 %}
<div class="tile is-ancestor mt-2">
    <div class="tile is-3">&nbsp;</div>
    <div class="tile is-4">
        <p class="control">
            <button type="submit" class="button is-primary">Kj&oslash;r sp&oslash;rring</button>
        </p>
        </form>
    </div>
</div>
<div class="block">&nbsp;</div>
{% endif %}

{% endblock %}

{% block se_bottom %}
{% endblock %}

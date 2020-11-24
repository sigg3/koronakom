{% extends "base.template" %}

{% block menu %}
  <div class="level-right ">
    <p class="level-item"><a href="https://din.kommune.nu" title="Hjem" class="button is-primary">Hjem</a></p>
    <p class="level-item"><a href="https://din.kommune.nu/utvalg" title="Utvalg" alt="Lag eget utvalg" class="button is-primary"><strong>Sp&oslash;rring</strong></a></p>
    <p class="level-item"><a href="https://din.kommune.nu/om" title="Om tjenesten" alt="Om tjenesten" class="button is-primary">Om tjenesten</a></p>
  </div>
{% endblock %}

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
<div class="tile is-ancestor mt-4 pt-4 pb-4">
    <div class="tile is-4">
        &nbsp;
    </div>
    <div class="tile is-4">
        <div class="container has-text-centered">
            <div class="level has-text-centered">
                {% if utvalg == 0 %}
                <p class="level-item"><a href="https://din.kommune.nu/hjelp" title="Hjelp med nøkler" class="button is-light">Nøkler</a></p>
                <p class="level-item"><a href="https://din.kommune.nu/utvalg" title="Velk kommuner enkeltvis" class="button is-info"><strong>Kommuner</strong></a></p>
                <p class="level-item"><a href="https://din.kommune.nu/fylker" title="Velg etter fylke" class="button is-light">Fylker</a></p>
                <p class="level-item"><a href="https://din.kommune.nu/egen" title="Egendefinert utvalg" class="button is-light">Egendefinert</a></p>
                {% elif utvalg == 1 %}
                <p class="level-item"><a href="https://din.kommune.nu/hjelp" title="Hjelp med nøkler" class="button is-light">Nøkler</a></p>
                <p class="level-item"><a href="https://din.kommune.nu/utvalg" title="Velk kommuner enkeltvis" class="button is-light">Kommuner</a></p>
                <p class="level-item"><a href="https://din.kommune.nu/fylker" title="Velg etter fylke" class="button is-info"><strong>Fylker</strong></a></p>
                <p class="level-item"><a href="https://din.kommune.nu/egen" title="Egendefinert utvalg" class="button is-light">Egendefinert</a></p>
                {% elif utvalg == 2 %}
                <p class="level-item"><a href="https://din.kommune.nu/hjelp" title="Hjelp med nøkler" class="button is-light">Nøkler</a></p>
                <p class="level-item"><a href="https://din.kommune.nu/utvalg" title="Velk kommuner enkeltvis" class="button is-light">Kommuner</a></p>
                <p class="level-item"><a href="https://din.kommune.nu/fylker" title="Velg etter fylke" class="button is-light">Fylker</a></p>
                <p class="level-item"><a href="https://din.kommune.nu/egen" title="Egendefinert utvalg" class="button is-info"><strong>Egendefinert</strong></a></p>
                {% else %}
                <p class="level-item"><a href="https://din.kommune.nu/hjelp" title="Hjelp med nøkler" class="button is-info"><strong>Nøkler</strong></a></p>
                <p class="level-item"><a href="https://din.kommune.nu/utvalg" title="Velk kommuner enkeltvis" class="button is-light">Kommuner</a></p>
                <p class="level-item"><a href="https://din.kommune.nu/fylker" title="Velg etter fylke" class="button is-light">Fylker</a></p>
                <p class="level-item"><a href="https://din.kommune.nu/egen" title="Egendefinert utvalg" class="button is-light">Egendefinert</a></p>
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
<form method="POST">
{% endif %}
<div class="tile is-ancestor mt-2">
    {% if utvalg == 0 %}
    <div class="tile is-2">&nbsp;</div>
    <div class="tile is-9">
    {% else %}
    <div class="tile is-4">&nbsp;</div>
    <div class="tile is-4">
    {% endif %}
        <div class="container">
            {% if utvalg == 0 %}
                {% for f, k in fylker.items() %}
                <h1 class="title">{{ f }}</h3>
                {% if f != "Oslo" %}
                    <div class="control">
                        <h2 class="subtitle">
                            Vis alle kommuner i {{ f }} fylke:
                            <label class="radio">
                                <input type="radio" name="{{ f }}"> Ja
                            </label>
                            <label class="radio">
                                <input type="radio" name="{{ f }}" checked> Nei
                                
                            </label>
                            <span class="has-text-grey-light">(overstyrer boksene)</span>
                        </h2>
                    </div>
                <div class="block">&nbsp;</div>
                {% endif %}
                {% for kommune in k %}
                <label class="checkbox" style="width: 14em;">
                    <input type="checkbox" name="{{ kommune[1] }}">
                    <a href="https://{{ kommune[0] }}.kommune.nu" title="{{ kommune[0] }}">{{ kommune[0] }}</a>
                </label>
                {% endfor %}
                <div class="block">&nbsp;</div>
                {% endfor %}
            {% elif utvalg == 1 %}
            <div class="container has-text-centered">
                <h2 class="subtitle">La meg se p&aring;:</h1>
                     <div class="control has-text-left ml-6 ">

                    {% for f, k in fylker.items() %}
                    <label class="checkbox" style="display: block;">
                        <input type="checkbox" name="{{ f }}">
                        <a href="https://sjekk.kommune.nu/{{ f }}" title="{{ f }}">{{ f }}</a>
                    </label>
                    {% endfor %}
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
                <h2 class="subtitle">Hjelp med søkeord / nøkler</h2>
                I utgangspunktet støtter søkemotoren følgende type oppslag:
                <div class="content">
                    <ul>
                        <li>navn på kommune (enkelt-oppslag)</li>
                        <li>&quot;&lt;kommune 1&gt; og &lt;kommune 2&gt;&quot; (sammenligning)</li>
                        <li>&quot;&lt;kommune 1&gt;, &lt;kommune 2&gt;, &lt;kommune 3&gt;, &lt;kommune 4&gt;&quot; (liste)</li>
                        <li>firesifret kommunenummer, e.g. 0301 for Oslo</li>
                        <li>N + firesifret postnummer, e.g. både N3401 (Lier) og 3411 (Sylling) går til Lier kommune (primær kommune)</li>
                        <li>navn på fylke (gir liste over kommunene)</li>
                    </ul>
                </div>
                <p>Man kan bruke <a href="https://din.kommune.nu/utvalg" title="Utvalg">Kommune-velgeren</a> til å gjøre større utvalg manuelt.</p>
                <p>Det er også lagt inn samme mulighet for fylker i <a href="https://din.kommune.nu/fylker" title="Fylker">fylke-velgeren</a>.</p>
                <p>Det er i tillegg mulig å få lagt inn egendefinerte spørringer, les mer om det på <a href="https://din.kommune.nu/egen" title="Egendefinerte søk">egendefinerte søk</a>.</p>
            {% endif %}

        </div>
    </div>
    <div class="tile is-1">
        &nbsp;
    </div>
</div>
{% if utvalg < 2 %}
<input type="submit">
</form>
{% endif %}

{% endblock %}

{% block se_bottom %}
{% endblock %}

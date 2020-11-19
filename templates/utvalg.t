{% extends "base.template" %}

{% block menu %}
  <div class="level-right ">
    <p class="level-item"><a href="/" title="Hjem" class="button is-primary">Hjem</a></p>
    <p class="level-item"><a href="/utvalg" title="Utvalg" alt="Lag eget utvalg" class="button is-primary"><strong>Sp&oslash;rring</strong></a></p>
    <p class="level-item"><a href="/om" title="Om tjenesten" alt="Om tjenesten" class="button is-primary">Om tjenesten</a></p>
  </div>
{% endblock %}

{% block tweety %}
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
                <p class="level-item"><a href="/utvalg" title="Velk kommuner enkeltvis" class="button is-info"><strong>Kommuner</strong></a></p>
                <p class="level-item"><a href="/fylker" title="Velg etter fylke" class="button is-light">Fylker</a></p>
                <p class="level-item"><a href="/egen" title="Egendefinert utvalg" class="button is-light">Egendefinert</a></p>
                {% elif utvalg == 1 %}
                <p class="level-item"><a href="/utvalg" title="Velk kommuner enkeltvis" class="button is-light">Kommuner</a></p>
                <p class="level-item"><a href="/fylker" title="Velg etter fylke" class="button is-info"><strong>Fylker</strong></a></p>
                <p class="level-item"><a href="/egen" title="Egendefinert utvalg" class="button is-light">Egendefinert</a></p>
                {% else %}
                <p class="level-item"><a href="/utvalg" title="Velk kommuner enkeltvis" class="button is-light">Kommuner</a></p>
                <p class="level-item"><a href="/fylker" title="Velg etter fylke" class="button is-light">Fylker</a></p>
                <p class="level-item"><a href="/egen" title="Egendefinert utvalg" class="button is-info"><strong>Egendefinert</strong></a></p>
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
                    <a href="/{{ kommune[2] }}" title="{{ kommune[0] }}">{{ kommune[0] }}</a>
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
                        <a href="/f/{{ f }}" title="{{ f }}">{{ f }}</a>
                    </label>
                    {% endfor %}
                </div>
            </div>
            {% else %}
                <h2 class="subtitle">Egendefinerte sp&oslash;rringer</h2>
                <p>Alle kommunene i Norge har en fire-sifret kode (f.eks. har Oslo 0301).</p>
                <p>&nbsp;</p>
                <p>Denne siden er ikke ferdig utviklet.</p>
                <p>&nbsp;</p>
                <p>Legg inn spørring for EU-risk-assessment</p>
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

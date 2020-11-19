{% extends "base.template" %}

{% block menu %}
  <div class="level-right ">
    <p class="level-item"><a href="/" title="Hjem" class="button is-primary">Hjem</a></p>
    <p class="level-item"><a href="/utvalg" title="Utvalg" alt="Lag eget utvalg" class="button is-primary"><strong>Sp&oslash;rring</strong></a></p>
    <p class="level-item"><a href="/om" title="Om tjenesten" alt="Om tjenesten" class="button is-primary">Om tjenesten</a></p>
  </div>
{% endblock %}
  
<div class="block">&nbsp;</div>



{% block sector_1 %}
<div class="tile is-ancestor mt-4 pt-4 pb-4">
    <div class="tile is-4">
        &nbsp;
    </div>
    <div class="tile is-4">
        <div class="container has-text-centered">
            <div class="level has-text-centered">
                <p class="level-item"><a href="/" title="Velk kommuner enkeltvis" class="button is-info"><strong>Kommuner</strong></a></p>
                <p class="level-item"><a href="/fylker" title="Velg etter fylke" class="button is-light">Fylker</a></p>
                <p class="level-item"><a href="/egen" title="Egendefinert utvalg" class="button is-light">Egendefinert</a></p>
            </div>
        </div>
    </div>
    <div class="tile is-4">
        &nbsp;
    </div>
</div>
{% endblock %}

{% block sector_2 %}
<div class="tile is-ancestor mt-2">
    <div class="tile is-2">
        &nbsp;
    </div>
    <div class="tile is-9">
        <div class="container">
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
                <a href="{{ kommune[2] }}" title="{{ kommune[0] }}">{{ kommune[0] }}</a>
            </label>
            {% endfor %}
            <div class="block">&nbsp;</div>
            {% endfor %}

        </div>
    </div>
    <div class="tile is-1">
        &nbsp;
    </div>
</div>

{% endblock %}

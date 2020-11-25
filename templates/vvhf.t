{% extends "base.template" %}

{% block menu %}
  <div class="level-right ">
    <p class="level-item"><a href="https://din.kommune.nu" title="Hjem" class="button is-primary">Hjem</a></p>
    <p class="level-item"><a href="https://sjekk.kommune.nu/" title="Utvalg" alt="Lag eget utvalg" class="button is-primary">Sp&oslash;rring</a></p>
    <p class="level-item"><a href="https://din.kommune.nu/om" title="Om tjenesten" alt="Om tjenesten" class="button is-primary">Om tjenesten</a></p>
  </div>
{% endblock %}


{% block sector_1 %}
<section class="section pt-2 pb-1">
    <div class="container has-text-centered">
        <h2 class="subtitle">{{ vvhf_sites[current]['title'] }}</h2>
        <div class="dropdown is-hoverable is-primary">
            <div class="dropdown-trigger">
                <button class="button has-icons-right" aria-haspopup="true" aria-controls="dropdown-menu3">
                    <span>Velg ønsket tabell</span>
                </button>
            </div>
            <div class="dropdown-menu" id="dropdown-menu3" role="menu">
                <div class="dropdown-content">
                {% for sykehus in vvhf_sites.keys() %}
                {% if vvhf_sites[sykehus]['url'] == current %}
                <a href="/{{ vvhf_sites[sykehus]['url'] }}" title="{{ vvhf_sites[sykehus]['title'] }}" class="dropdown-item is-active">{{ vvhf_sites[sykehus]['title'] }}</a>
                {% else %}
                <a href="/{{ vvhf_sites[sykehus]['url'] }}" title="{{ vvhf_sites[sykehus]['title'] }}" class="dropdown-item">{{ vvhf_sites[sykehus]['title'] }}</a>
                {% endif %}
                {% endfor %}
                </div>
            </div>
        </div>
    </div>
</section>
{% endblock %}

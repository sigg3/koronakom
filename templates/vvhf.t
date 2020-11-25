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
        <h2 class="subtitle">Oppdatert {{ nordate }}</h2>
        <div class="dropdown is-hoverable is-primary">
            <div class="dropdown-trigger">
                <button class="button has-icons-right" aria-haspopup="true" aria-controls="dropdown-menu3">
                    <span>Velg ønsket tabell</span>
                </button>
            </div>
            <div class="dropdown-menu" id="dropdown-menu3" role="menu">
                <div class="dropdown-content">
                {% for sykehus in vvhf_sites.keys() %}
                {% if vvhf_sites[sykehus]['url'] == "vvhf" %}
                <a href="/" title="{{ vvhf_sites[sykehus]['title'] }}" class="dropdown-item">{{ vvhf_sites[sykehus]['title'] }}</a>
                {% else %}
                <a href="/?vis={{ vvhf_sites[sykehus]['url'] }}" title="{{ vvhf_sites[sykehus]['title'] }}" class="dropdown-item">{{ vvhf_sites[sykehus]['title'] }}</a>
                {% endif %}
                {% endfor %}
                </div>
            </div>
        </div>
    </div>
    <div class="tile is-ancestor">
        {% for table in result_dict.keys() %}
        <div class="tile is-3">&nbsp;</div>
        <div class="tile is-6">
            <div class="block">&nbsp;</div>
            {% if result_dict[table]['risk'] == 0 %}
            <table class="table is-fullwidth is-hoverable has-background-success-light">
            {% elif result_dict[table]['risk'] == 1 %}
            <table class="table is-fullwidth is-hoverable has-background-warning-light">
            {% elif result_dict[table]['risk'] == 2 %}
            <table class="table is-fullwidth is-hoverable has-background-danger-light">
            {% else %}
            <table class="table is-fullwidth is-hoverable">
            {% endif %}
                <thead>
                    <tr>
                        <th>{{ result_dict[table]['name'] }} siste</th>
                        <th class="has-text-right">14 dager</th>
                        <th class="has-text-right">7 dager</th>
                        <th class="has-text-right">3 dager</th>
                        <th class="has-text-right">24 timer</th>
                    </tr>
                </thead>
                <tbody>
                    <tr>
                        <th>tilfeller</th>
                        {% for v in result_dict[table]['diff_n'] %}
                        {% if loop.index0 == 0 %}
                        {% if result_dict[table]['risk'] == 0 %}
                        <td class="has-text-right has-background-success">{{ v }}</td>
                        {% if result_dict[table]['risk'] == 1 %}
                        <td class="has-text-right has-background-warning">{{ v }}</td>
                        {% if result_dict[table]['risk'] == 2 %}
                        <td class="has-text-right has-background-danger">{{ v }}</td>
                        {% else %}
                        <td class="has-text-right">{{ v }}</td>
                        {% endif %}
                        {% else %}
                        <td class="has-text-right">{{ v }}</td>
                        [% endif %}
                        {% endfor %}
                    </tr>
                    <tr>
                        <th>per 100k</th>
                        {% for v in result_dict[table]['diff_100k'] %}
                        {% if v is number %}
                        <td class="has-text-right">{{ "{:.2f}".format(v) }}</td>
                        {% else %}
                        <td class="has-text-right">{{ v }}</td>
                        {% endif %}
                        {% endfor %}
                    </tr>
                </tbody>
            </table>
            <div class="block">&nbsp;</div>
        </div>
        <div class="tile is-3">&nbsp;</div>
        {% endfor %}
    </div>
</section>
{% endblock %}

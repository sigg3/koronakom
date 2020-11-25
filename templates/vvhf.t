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
        <div class="tile is-3">&nbsp;</div>
        <div class="tile is-6">
            <table class="table is-fullwidth is-hoverable">
                <thead>
                    <tr>
                        <th>Utvikling siste</th>
                        <th class="has-text-right">14 dager</th>
                        <th class="has-text-right">7 dager</th>
                        <th class="has-text-right">3 dager</th>
                        <th class="has-text-right">24 timer</th>
                    </tr>
                </thead>
                <tbody>
                    {% for table in result_dict.keys() %}
                    {% if result_dict[table]['risk'] == 0 %}
                    <tr class="has-background-success">
                    {% elif result_dict[table]['risk'] == 1 %}
                    <tr class="has-background-warning">
                    {% elif result_dict[table]['danger'] == 2 %}
                    <tr class="has-background-danger">
                    {% else %}
                    <tr>
                    {% endif %}
                        <th>{{ result_dict[table]['name'] }}</th>
                        <td colspan="4">&nbsp;</td>
                    </tr>
                    <tr>
                        <th>tilfeller</th>
                        {% for v in result_dict[table]['diff_n'] %}
                        <td class="has-text-right">{{ v }}</td>
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
                    <tr>
                        <td colspan="5">
                            <div class="block">&nbsp;</div>
                        </td>
                    </tr>
                        
                    {% endfor %}
                </tbody>
            </table>
        </div>
        <div class="tile is-3">&nbsp;</div>
    </div>
</section>
{% endblock %}

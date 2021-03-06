{% extends "base.template" %}

{% block sector_1 %}
<section class="section pt-2 pb-1">
    <div class="container has-text-centered">
        <h2 class="subtitle">Sortert etter nye tilfeller per 100k. Oppdatert: {{ nordate }}</h2>
        <div class="dropdown is-hoverable is-primary has-text-left">
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
    <div class="block mt-3 mb-3">
        &nbsp;
    </div>
    <div class="tile is-ancestor">
        <div class="tile is-3">&nbsp;</div>
        <div class="tile is-6">
            <div class="block">&nbsp;</div>            
            <table class="table is-fullwidth">
            {% for table in result_dict.keys() %}
                <tr>
                    <td class="border: 0;" colspan="5">
                        <div class="block">&nbsp;</div>
                        <span class="is-size-3"><a href="https://{{ result_dict[table]['url'] }}" title="{{ result_dict[table]['name'] }} kommune" class="has-text-black">{{ result_dict[table]['name'] }}</a></span>
                    </td>
                </tr>
                {% if result_dict[table]['risk'] == 0 %}
                <tr class="has-background-success-light">
                {% elif result_dict[table]['risk'] == 1 %}
                <tr class="has-background-warning-light">
                {% elif result_dict[table]['risk'] == 2 %}
                <tr class="has-background-danger-light">
                {% else %}
                <tr>
                {% endif %}
                    <td>&nbsp;</th>
                    <td class="has-text-right"><strong>14 dager</strong></td>
                    <td class="has-text-right"><strong>7 dager</strong></td>
                    <td class="has-text-right"><strong>3 dager</strong></td>
                    <td class="has-text-right"><strong>24 timer</strong></td>
                </tr>
                {% if result_dict[table]['risk'] == 0 %}
                <tr class="has-background-success-light">
                {% elif result_dict[table]['risk'] == 1 %}
                <tr class="has-background-warning-light">
                {% elif result_dict[table]['risk'] == 2 %}
                <tr class="has-background-danger-light">
                {% else %}
                <tr>
                {% endif %}
                    <th>nye</th>
                    {% for v in result_dict[table]['diff_n'] %}
                    <td class="has-text-right">{{ v }}</td>
                        {% endfor %}
                </tr>
                {% if result_dict[table]['risk'] == 0 %}
                <tr class="has-background-success-light">
                {% elif result_dict[table]['risk'] == 1 %}
                <tr class="has-background-warning-light">
                {% elif result_dict[table]['risk'] == 2 %}
                <tr class="has-background-danger-light">
                {% else %}
                <tr>
                {% endif %}
                    <th>per 100k</th>
                    {% for v in result_dict[table]['diff_100k'] %}
                    {% if v is number %}
                    {% if loop.index0 == 0 %}                        
                    {% if result_dict[table]['risk'] == 0 %}
                    <td class="has-text-right has-background-success">
                    {% elif result_dict[table]['risk'] == 1 %}
                    <td class="has-text-right has-background-warning">
                    {% elif result_dict[table]['risk'] == 2 %}
                    <td class="has-text-right has-background-danger has-text-white">
                    {% else %}
                    <td class="has-text-right">
                    {% endif %}
                    
                    <strong>{{ "{:.2f}".format(v) }}</strong>
                    </td>
                    {% else %}
                    <td class="has-text-right">{{ "{:.2f}".format(v) }}</td>
                    {% endif %}
                    {% else %}
                    <td class="has-text-right">{{ v }}</td>
                    {% endif %}
                    {% endfor %}
                </tr>
                {% endfor %}
            </table>
            <div class="block">&nbsp;</div>
        </div>
        <div class="tile is-3">&nbsp;</div>
    </div>
</section>
{% endblock %}


{% block se_bottom %}
{% endblock %}

{% extends "base.template" %}

  {% block menu %}
  <div class="level-right ">
    <p class="level-item"><a href="/" title="Hjem" class="button is-primary">Hjem</a></p>
    <p class="level-item"><a href="/utvalg" title="Utvalg" alt="Lag eget utvalg" class="button is-primary">Sp&oslash;rring</a></p>
    <p class="level-item"><a href="/om" title="Om tjenesten" alt="Om tjenesten" class="button is-primary">Om tjenesten</a></p>
  </div>
  {% endblock %}

<div class="block">&nbsp;</div>

{% block sector_1 %}
{% for table in result_dict.keys() %}
{% if only_one %} 
<div class="tile is-ancestor mt-4 pt-8">
    <div class="tile is-3">
        &nbsp;
    </div>
    <div class="tile is-5">
        <table class="table is-fullwidth">
          <thead>
            <tr>
              <th>Utvikling siste</th>
              <th class="has-text-right">to uker</th>
              <th class="has-text-right">uke</th>
              <th class="has-text-right">3 dager</th>
              <th class="has-text-right">24 timer</th>
            </tr>
          </thead>
          <tbody>
            <tr>
               <th>tilfeller</th>
               {% for v in result_dict[table]['diff_n'] %}
               <td class="has-text-right">{{ v }}</td>
               {% endfor %}
            </tr>
            <tr>
               <th>per 100k</th>
               {% for v in result_dict[table]['diff_100k'] %}
               <td class="has-text-right">{{ "{:.2f}".format(v) }}</td>
               {% endfor %}
            </tr>
          </tbody>
        </table>
    </div>
    <div class="tile is-1">
        &nbsp;
    </div>
    <div class="tile is-2">
    {% if result_dict[table]['risk'] == 0 %}
    <article class="notification is-success">
    {% elif result_dict[table]['risk'] == 1 %}
    <article class="notification is-warning">
    {% elif result_dict[table]['risk'] == 2 %}
    <article class="notification is-danger">
    {% elif result_dict[table]['risk'] == 1 %}
    <article class="notification white">
    {% endif %}
        <p class="title is-large">
            <strong>
            {% if result_dict[table]['risk'] == 0 %}
            gr&oslash;nt
            {% elif result_dict[table]['risk'] == 1 %}
            oransje
            {% elif result_dict[table]['risk'] == 2 %}
            r&oslash;dt
            {% else %}
            uklassifisert
            {% endif %}
            </strong>
        </p>
        <p class="is-size-2">omr&aring;de</p>
    </article>
    </div>
    <div class="tile is-1">
        &nbsp;
    </div>
</div>


{% elif exactly_two %}
<div class="block">&nbsp;</div>
<div class="tile is-ancestor">
    <div class="tile is-vcentered is-3">
        <div class="container has-text-right pr-3">
            <div class="block">&nbsp;</div>
            <h1 class="title">
                {% if result_dict[table]['alt'] %}{{ result_dict[table]['alt'] }}
                {% else %}
                {{ result_dict[table]['name'] }}
                {% endif %}
            </h1>
            <h4 class="subtitle is-lowercase">
                <a href="{{ result_dict[table]['url'] }}" title="{{ result_dict[table]['name'] }}">{{ result_dict[table]['name'] }}.kommune.nu</a>
            </h4>
        </div>
    </div>
    <div class="tile is-6">
        <table class="table is-size-5">
          <thead>
            <tr>
              <th>Utvikling</th>
              <th>siste to uker</th>
              <th>siste uken</th>
              <th>siste tre dager</th>
              <th>siste 24 timer</th>
            </tr>
          </thead>
          <tbody>
            <tr>
               <th>tilfeller</th>
               {% for v in result_dict[table]['diff_n'] %}
               <td class="has-text-right">{{ v }}</td>
               {% endfor %}
            </tr>
            <tr>
               <th>per 100k</th>
               {% for v in result_dict[table]['diff_100k'] %}
               <td class="has-text-right">{{ "{:.2f}".format(v) }}</td>
               {% endfor %}
            </tr>
          </tbody>
        </table>
    </div>
    <div class="tile is-1">
        <div class="tile mt-2">
                {% if result_dict[table]['risk'] == 0 %}
                <article class="notification is-success">
                {% elif result_dict[table]['risk'] == 1 %}
                <article class="notification is-warning">
                {% elif result_dict[table]['risk'] == 2 %}
                <article class="notification is-danger">
                {% elif result_dict[table]['risk'] == 1 %}
                <article class="notification white">
                {% endif %}
                    <p class="title is-size-5">
                        <strong >
                        {% if result_dict[table]['risk'] == 0 %}
                        gr&oslash;nt
                        {% elif result_dict[table]['risk'] == 1 %}
                        oransje
                        {% elif result_dict[table]['risk'] == 2 %}
                        r&oslash;dt
                        {% else %}
                        N / A
                        {% endif %}
                        </strong>
                    </p>
                    <p class="is-size-5">omr&aring;de</p>
                </article>
        </div>
    </div>
    <div class="tile is-2">
        &nbsp;
    </div>
</div>

{% else %}

<div class="block">&nbsp;</div>
<div class="container">
    <div class="columns">
        <div class="column is-one-fifth">
            &nbsp;
        </div>
        <div class="column">
            <h1 class="title">
            {% if result_dict[table]['alt'] %}{{ result_dict[table]['alt'] }}
            {% else %}
            {{ result_dict[table]['name'] }}
            {% endif %}
            {% if result_dict[table]['risk'] == 0 %}
             <span class="tag is-success is-medium" title="gr&oslash;nt omr&aring;de">gr&oslash;nn</span>
            {% elif result_dict[table]['risk'] == 1 %}
            <span class="tag is-warning is-medium" title="oransje omr&aring;de">oransje</span></h1>
            {% elif result_dict[table]['risk'] == 2 %}
            <span class="tag is-danger is-medium" title="r&oslash;dt omr&aring;de">r&oslash;d</span></h1>
            {% endif %}
            </h1>
            <h6 class="subtitle">
                Lenke:
                <a href="/k/{{ result_dict[table]['name'] }}" title="{{ result_dict[table]['name'] }}">kommune</a>, 
                <a href="/f/{{ result_dict[table]['fylke'] }}" title="{{ result_dict[table]['fylke'] }}">fylke</a>
            </h6>
        </div>
    </div>
    <div class="columns">
        <div class="column is-one-fifth">
            &nbsp;
        </div>
        <div class="column">
            <table class="table is-size-5">
               <thead>
                  <tr>
                    <th>Utvikling</th>
                    <th>siste to uker</th>
                    <th>siste uken</th>
                    <th>siste tre dager</th>
                    <th>siste 24 timer</th>
                  </tr>
                </thead>
                <tbody>
                  <tr>
                    <th>tilfeller</th>
                     {% for v in result_dict[table]['diff_n'] %}
                     <td class="has-text-right">{{ v }}</td>
                     {% endfor %}
                  </tr>
                  <tr>
                     <th>per 100k</th>
                     {% for v in result_dict[table]['diff_100k'] %}
                     <td class="has-text-right">{{ "{:.2f}".format(v) }}</td>
                     {% endfor %}
                 </tr>
                </tbody>
            </table>
        </div>
    </div>
</div>
{% endif %}
{% endfor %}

<div class="tile is-ancestor mt-4 pt-8">
    <div class="tile is-2">&nbsp;</div>
    <div class="tile is-8">
        <div class="container">
            <div class="content has-text-centered">
                <p class="help">Hva betyr tallene? F&aring; svar p&aring; sp&oslash;rsm&aring;l <a href="/om" title="Om tjenesten">om korona-tallene her</a>.</p>
            </div>
        </div>
    </div>
    <div class="tile is-2">&nbsp;</div>
</div>
{% endblock %}


{% block sector_2 %}
{% for table in result_dict.keys() %}
{% if only_one %}
<!-- do showcase of muncipality -->
<!-- homepage, stats, direct link -->



<div class="tile is-ancestor mb-6 mt-6 pb-4 pt-2">
    <div class="tile is-4">
        &nbsp;
    </div>
    <div class="tile is-5">
        <div class="tile box">
            <table class="table is-fullwidth">
                <caption><strong>{{ result_dict[table]['name'] }} kommune</strong> (<a href="/f/{{ result_dict[table]['fylke'] }}" title="{{ result_dict[table]['fylke'] }}">{{ result_dict[table]['fylke'] }}</a>)</caption>
                <tr>
                    <th><strong>Oppdatert</th>
                    <td>{{ nordate }}</td>
                </tr>
                <tr>
                    <th><strong>Hjemmeside</strong></th>
                    <td><a href="{{ result_dict[table]['web'] }}" title="{{ result_dict[table]['name'] }} hjemmeside">{{ result_dict[table]['web'] }}</a></td>
                </tr>
                <tr>
                    <th><strong>Statistikk</strong></th>
                    <td><a href="{{ result_dict[table]['ssb'] }}" title="{{ result_dict[table]['name'] }} faktaside">{{ result_dict[table]['ssb']}}</a></td>
                </tr>
                <tr>
                    <th>Lenke hit</th>
                    <td><a href="{{ result_dict[table]['url'] }}" title="{{ result_dict[table]['name'] }}">{{ result_dict[table]['url'] }}</a></td>
                </tr>
            </table>
        </div>
    </div>
    <div class="tile is-3">
        &nbsp;
    </div>
</div>
{% endif %}
{% endfor %}
{% endblock %}



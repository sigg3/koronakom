{% extends "base.template" %}
{% block tweety %}
<nav class="level">
  <div class="level-item has-text-centered">
    <div>
      <p class="heading">Nye smittede</p>
      <p class="title">{{ diff_n }}</p>
    </div>
  </div>
  <div class="level-item has-text-centered">
    <div>
      <p class="heading">Kommuner med smitte</p>
      <p class="title">{{ infected }}</p>
    </div>
  </div>
  <div class="level-item has-text-centered">
    <div>
      <p class="heading">Røde</p>
      <p class="title">{{ red }}</p>
    </div>
  </div>
  <div class="level-item has-text-centered">
    <div>
      <p class="heading">Oransje</p>
      <p class="title">{{ orange }}</p>
    </div>
  </div>
  <div class="level-item has-text-centered">
    <div>
      <p class="heading">Gr&oslash;nne</p>
      <p class="title">{{ green }}</p>
    </div>
  </div>
</nav>
{% endblock %}
{% block sector_1 %}
<section class="section pt-2 pb-1">
    <div class="container">
        <h1 class="title"><em>din</em>.kommune.nu</h1>
        <h2 class="subtitle">
            Dette er en oppslagstjeneste for &aring; enkelt kunne <strong>sjekke gjeldende korona status</strong> for din kommune, ditt fylke eller landet forøvrig.
            Tallene hentes daglig fra Folkehelseinstituttet og ble 
            {% if updated == real_today %}
            <span class="tag is-success is-light is-medium">
            {% else %}
            <span class="tag is-info is-light is-medium">
            {% endif %}
            sist oppdatert {{ nordate }}.</span> <a href="https://din.kommune.nu/om" title="Om tall og tjenesten">Les mer her</a>.
            Bruk søkemotoren under eller lag <a href="https://sjekk.kommune.nu/hjelp" title="Sp&oring;rring">din egen spørring</a>.
        </h2>
    </div>
</section>
{% endblock %}
{% block sector_2 %}
<section class="section">
  <div class="container">
    <h1 class="title">Statistikk over fylker og kommuner i Norge</h1>
    <h2 class="subtitle">
         Siden 2020 er det 11 fylker og 356 kommuner i landet v&aring;rt. Klikk p&aring; ditt fylke for &aring; se de mest relevante korona-tallene:
         <a href="https://agder-fylke.kommune.nu" title="Agder">Agder</a>,
         <a href="https://innlandet-fylke.kommune.nu" title="Innlandet">Innlandet</a>,
         <a href="https://more-og-romsdal-fylke.kommune.nu" title="M&oslash;re og Romsdal">Møre og Romsdal</a>,
         <a href="https://nordland-fylke.kommune.nu" title="Nordland - Nordlánnda">Nordland - Nordlánnda</a>,
         <a href="https://oslo-fylke.kommune.nu" title="Oslo">Oslo</a>,
         <a href="https://rogaland-fylke.kommune.nu" title="Rogaland">Rogaland</a>,
         <a href="https://troms-og-finnmark.kommune.nu" title="Troms og Finnmark - Romsa ja Finnmárku - Tromssa ja Finmarkku">Troms og Finnmark - Romsa ja Finnmárku - Tromssa ja Finmarkku</a>,
         <a href="https://trondelag-fylke.kommune.nu" title="Trøndelag - Trööndelage">Trøndelag - Trööndelage</a>,
         <a href="https://vestfold-og-telemark-fylke.kommune.nu" title="Vestfold og Telemark">Vestfold og Telemark</a>,
         <a href="https://vestland-fylke.kommune.nu" title="Vestland">Vestland</a>,
         og <a href="https://viken-fylke.kommune.nu" title="Viken">Viken</a>.</h2>
         <h2 class="subtitle">
         Per {{ nordate }} er det registrert korona i {{ infected }} av 356 kommuner. Sjekk din kommune under:
    </h2>
  </div>
</section>
{% endblock %}


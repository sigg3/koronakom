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
            Denne siden er en oppslagstjeneste for &aring; enkelt kunne <strong>sjekke gjeldende korona status</strong> for sin kommune, sitt fylke eller landet forøvrig.
            Tallene hentes daglig fra Folkehelseinstituttet og ble sist oppdatert {{ nordate }}. <a href="/om" title="Om tall og tjenesten">Les mer her</a>.
            Bruk søkemotoren under eller lag <a href="https://sjekk.kommune.nu" title="Sp&oring;rring">din egen spørring</a>.
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
 <a href="/f/Agder" title="Agder">Agder</a>,
 <a href="/f/Innlandet" title="Innlandet">Innlandet</a>,
 <a href="/f/M&oslash;re og Romsdal" title="M&oslash;re og Romsdal">Møre og Romsdal</a>,
 <a href="/f/Nordland" title="Nordland - Nordlánnda">Nordland - Nordlánnda</a>,
 <a href="/f/Oslo" title="Oslo">Oslo</a>,
 <a href="/f/Rogaland" title="Rogaland">Rogaland</a>,
 <a href="/f/Troms og Finnmark" title="Troms og Finnmark - Romsa ja Finnmárku - Tromssa ja Finmarkku">Troms og Finnmark - Romsa ja Finnmárku - Tromssa ja Finmarkku</a>,
 <a href="/f/Tr&oslash;ndelag" title="Trøndelag - Trööndelage">Trøndelag - Trööndelage</a>,
 <a href="/f/Vestfold og Telemark" title="Vestfold og Telemark">Vestfold og Telemark</a>,
 <a href="/f/Vestland" title="Vestland">Vestland</a>,
 og <a href="/f/Viken" title="Viken">Viken</a>.</j2>
 <h2 class="subtitle">
         Per {{ nordate }} er det registrert korona i {{ infected }} av 356 kommuner. Sjekk din kommune under:

    </h2>
  </div>
</section>
{% endblock %}


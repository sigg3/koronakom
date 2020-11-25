{% extends "base.template" %}

{% block menu %}
  <div class="level-right ">
    <p class="level-item"><a href="https://din.kommune.nu" title="Hjem" class="button is-primary">Hjem</a></p>
    <p class="level-item"><a href="https://din.kommune.nu/utvalg" title="Utvalg" alt="Lag eget utvalg" class="button is-primary">Sp&oslash;rring</a></p>
    <p class="level-item"><a href="https://din.kommune.nu/om" title="Om tjenesten" alt="Om tjenesten" class="button is-primary"><strong>Om tjenesten</strong></a></p>
  </div>
{% endblock %}

{% block sector_1 %}
<section class="section pt-2 pb-1">
    <div class="container">
        <h2 class="title">Tallene p&aring; siden</h2>
        <p>Tallmaterialet p&aring; denne siden kommer ikke overraskende fra <a href="https://www.fhi.no/" title="Folkehelseinstituttet FHI"><span class="tag is-warning is-medium">Folkehelseinstituttet FHI</span></a> som samler det inn via Meldingssystem for smittsomme sykdommer (MSIS).</p>
        <div class="content">
            <ul>
                <li>For detaljert, interaktiv oversikt fra <span class="tag is-warning is-medium">FHI</span> med nøkkeltall for dag og uke, <a href="https://www.fhi.no/sv/smittsomme-sykdommer/corona/dags--og-ukerapporter/dags--og-ukerapporter-om-koronavirus/" title="Dags og ukerapporter om koronavirus">følg denne lenken</a>.</li>
                <li>For mer informasjon om overvåking av SARS-CoV-2 og statistikken <span class="tag is-warning is-medium">FHI</span> kan tilby, <a href="https://www.fhi.no/sv/smittsomme-sykdommer/corona/dags--og-ukerapporter/sporsmal-og-svar-om-koronaovervaking-og-statistikk/" title="Spørsmål og svar om koronastatistikken og de interaktive diagrammene">klikk her</a>.</li>
            </ul>
        </div>
        <p><span class="tag is-primary is-light is-medium"><strong>kommune.nu</strong></span> baserer seg utelukkende på <strong>tall for de siste 14 dagene som hentes hver dag rundt kl. 13.</strong> Dette er en frivillig, ikke-kommersiell tjeneste som er laget for &aring; raskt kunne: sjekke enhver kommune; sammenligne kommuner; sjekke tilstanden i fylket; og lage og lagre egne sp&oslash;rringer. Innplasssering av omr&aring;der inn i kategoriene <span class="tag is-success">gr&oslash;nn</span>, <span class="tag is-warning">oransje</span> eller <span class="tag is-danger">r&oslash;d</span> f&oslash;lger i grove trekk anbefalingene til EUs <span class="tag is-info is-medium" alt="European Centre for Disease Prevention and Control">ECDC</span> som man <a href="https://www.ecdc.europa.eu/en/covid-19/situation-updates/weekly-maps-coordinated-restriction-free-movement" title="Maps in support of the Council Recommendation on a coordinated approach to the restriction of free movement in response to the COVID-19 pandemic in the EU/EEA and the UK">finner her</a>.</p>
    </div>
</section>
<section class="section">
    <div class="container">
        <h2 class="title">Om tjenesten</h2>
        <p>Den minste bestanddelen p&aring; <span class="tag is-primary is-light is-medium"><strong>kommune.nu</strong></span> er <em>kommunen</em>. Man kan spørre etter enkelte kommuner, etter fylker eller sammenligne <a href="https://sjekk.kommune.nu/?s=Karasjok+og+stavanger" titl="Karasjok og Stavanger">tilfeldig utvalgte kommuner</a>. For eksempel kan man sjekke <a href="https://sjekk.kommune.nu/?s=E6" title="sjekk korona status for E6 sørover">alle kommunene langs E6</a>. Klikk på lenken <a href="https://sjekk.kommune.nu/utvalg" title="utvalg">sp&oslash;rring</a> for å gjøre arbitrære utvalg.</p>
        <p>Jeg mottar med takk oversettelser av fraser og linjer med tekst fra <span class="tag is-primary is-light is-medium"><strong>kommune.nu</strong></span> til andre språk. Hvis du er interessert i å oversette fra norsk eller engelsk til f.eks. samisk, kvensk, polsk etc. så er dette absolutt verdifullt. <a href="https://github.com/sigg3/koronakom/issues" title="github issues">Ta kontakt med meg her</a>. Oversettelser kan gjøres i programvare eller i notisblokk (så legger jeg det inn eventuelt).</p>
    </div>
</section>
<section class="section">
    <div class="container">
        <h2 class="title">Teknisk og juridisk</h2>
        <p>Denne websiden eller &laquo;appen&raquo; best&aring;r hovedsaklig av <strong>Python 3</strong> skrevet av undertegnede, og som leveres v.h.a. <strong><a href="https://www.starlette.io" title="Starlette">Starlette</a></strong> med <strong><a href="https://jinja.palletsprojects.com/en/2.11.x/" title="Jinja">jinja2</a></strong> maler og <strong><a href="https://bulma.io/" title="Bulma CSS">Bulma CSS</a></strong>. <span class="tag is-warning">Det finnes ikke JavaScript på siden.</span></p>
        <p>Kildekoden er <strong><a href="https://www.gnu.org/philosophy/free-sw.html" title="What is Free Software?">fri programvare</a></strong> og distribueres under <a href="https://www.gnu.org/licenses/agpl-3.0.html" title="GNU Affero License 3.0"><span class="tag is-light is-medium">GNU Affero License</span></a> versjon 3. Med andre ord: ikke skyld på meg hvis det ikke virker, men <a href="https://github.com/sigg3/koronakom/issues" title="github issues">gi meg gjerne beskjed</a>!
        <div class="container has-text-centered">
            <span class="icon">
                <svg class="svg-inline--fa fa-github fa-w-16" aria-hidden="true" focusable="false" data-prefix="fab" data-icon="github" role="img" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 496 512" data-fa-i2svg="">
                    <path fill="currentColor" d="M165.9 397.4c0 2-2.3 3.6-5.2 3.6-3.3.3-5.6-1.3-5.6-3.6 0-2 2.3-3.6 5.2-3.6 3-.3 5.6 1.3 5.6 3.6zm-31.1-4.5c-.7 2 1.3 4.3 4.3 4.9 2.6 1 5.6 0 6.2-2s-1.3-4.3-4.3-5.2c-2.6-.7-5.5.3-6.2 2.3zm44.2-1.7c-2.9.7-4.9 2.6-4.6 4.9.3 2 2.9 3.3 5.9 2.6 2.9-.7 4.9-2.6 4.6-4.6-.3-1.9-3-3.2-5.9-2.9zM244.8 8C106.1 8 0 113.3 0 252c0 110.9 69.8 205.8 169.5 239.2 12.8 2.3 17.3-5.6 17.3-12.1 0-6.2-.3-40.4-.3-61.4 0 0-70 15-84.7-29.8 0 0-11.4-29.1-27.8-36.6 0 0-22.9-15.7 1.6-15.4 0 0 24.9 2 38.6 25.8 21.9 38.6 58.6 27.5 72.9 20.9 2.3-16 8.8-27.1 16-33.7-55.9-6.2-112.3-14.3-112.3-110.5 0-27.5 7.6-41.3 23.6-58.9-2.6-6.5-11.1-33.3 2.6-67.9 20.9-6.5 69 27 69 27 20-5.6 41.5-8.5 62.8-8.5s42.8 2.9 62.8 8.5c0 0 48.1-33.6 69-27 13.7 34.7 5.2 61.4 2.6 67.9 16 17.7 25.8 31.5 25.8 58.9 0 96.5-58.9 104.2-114.8 110.5 9.2 7.9 17 22.9 17 46.4 0 33.7-.3 75.4-.3 83.6 0 6.5 4.6 14.4 17.3 12.1C428.2 457.8 496 362.9 496 252 496 113.3 383.5 8 244.8 8zM97.2 352.9c-1.3 1-1 3.3.7 5.2 1.6 1.6 3.9 2.3 5.2 1 1.3-1 1-3.3-.7-5.2-1.6-1.6-3.9-2.3-5.2-1zm-10.8-8.1c-.7 1.3.3 2.9 2.3 3.9 1.6 1 3.6.7 4.3-.7.7-1.3-.3-2.9-2.3-3.9-2-.6-3.6-.3-4.3.7zm32.4 35.6c-1.6 1.3-1 4.3 1.3 6.2 2.3 2.3 5.2 2.6 6.5 1 1.3-1.3.7-4.3-1.3-6.2-2.2-2.3-5.2-2.6-6.5-1zm-11.4-14.7c-1.6 1-1.6 3.6 0 5.9 1.6 2.3 4.3 3.3 5.6 2.3 1.6-1.3 1.6-3.9 0-6.2-1.4-2.3-4-3.3-5.6-2z"></path>
                </svg><!-- <i class="fab fa-github"></i> -->
                <a href="https://github.com/sigg3/koronakom" title="Koronakom på Github">Koronakom</a>
            </span>
        </div>
    </div>
</section>
{% endblock %}

{% block se_bottom %}
{% endblock %}

{% extends "base.template" %}


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
    </div>
    <div class="container has-text-centered">
        <a href="https://github.com/sigg3/koronakom" title="Koronakom på Github" class="has-text-white"><button class="button is-success is-rounded">github: <strong>Koronakom</strong></button></a>
    </div>
    
    
    
</section>
{% endblock %}

{% block se_bottom %}
{% endblock %}

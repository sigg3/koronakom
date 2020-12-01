{% extends "upper.t" %}
  <!-- Right side -->
  {% block menu %}
  <div class="level-right is-grouped-right is-hidden-tablet"> <!-- cell-phone only -->
    <p class="level-item"><a href="https://din.kommune.nu" title="Hjem" class="button is-primary"><strong>Hjem</strong></a></p>
    <p class="level-item"><a href="https://sjekk.kommune.nu/hjelp" title="Sp&oslash;rring" alt="Lag eget utvalg" class="button is-primary">Sp&oslash;rring</a></p>
    <p class="level-item"><a href="https://din.kommune.nu/om" title="Om tjenesten" alt="Om tjenesten" class="button is-primary">Om</a></p>
    <p class="level-item">&nbsp;</p><!-- bugfix -->
  </div>
  <div class="level-right is-grouped-right is-hidden-mobile"> <!-- any other viewer -->
    <p class="level-item"><a href="https://din.kommune.nu" title="Hjem" class="button is-primary"><strong>Hjem</strong></a></p>
    <p class="level-item"><a href="https://sjekk.kommune.nu/hjelp" title="Sp&oslash;rring" alt="Lag eget utvalg" class="button is-primary">Sp&oslash;rring</a></p>
    <p class="level-item"><a href="https://din.kommune.nu/om" title="Om tjenesten" alt="Om tjenesten" class="button is-primary">Om tjenesten</a></p>
  </div>
  {% endblock %}
</nav>
    <div class="container has-text-centered">
      <h1 class="title is-uppercase is-2">
        <a href="{{ hero_link }}" title="{{ hero_title }}" class="has-text-black">{{ hero_title }}</a>
      </h1>
      <h2 class="subtitle is-3">
        {{ hero_subtitle }}
      </h2>
    </div>
  </div>
</section>

{% extends "base.template" %}

{% block menu %}
  <div class="level-right ">
    <p class="level-item"><a href="https://din.kommune.nu" title="Hjem" class="button is-primary">Hjem</a></p>
    <p class="level-item"><a href="https://sjekk.kommune.nu/" title="Utvalg" alt="Lag eget utvalg" class="button is-primary">Sp&oslash;rring</a></p>
    <p class="level-item"><a href="https://din.kommune.nu/om" title="Om tjenesten" alt="Om tjenesten" class="button is-primary">Om tjenesten</a></p>
  </div>
{% endblock %}



{% block sector_1 %}
<section>
<div class="tile is-ancestor mt-4 pt-8">
    <div class="tile is-3">
        &nbsp;
    </div>
    <div class="tile is-5">
        <div class="dropdown">
            <div class="dropdown-trigger">
                <button class="button" aria-haspopup="true" aria-controls="dropdown-menu3">
                    <span>Click me</span>
                    <span class="icon is-small">
                    <i class="fas fa-angle-down" aria-hidden="true"></i>
                    </span>
                </button>
          </div>
          <div class="dropdown-menu" id="dropdown-menu3" role="menu">
            <div class="dropdown-content">
                <a href="#" class="dropdown-item">Overview</a>
                <a href="#" class="dropdown-item">Modifiers</a>
                {% for key in vvhf_sites %}
                <hr class="dropdown-divider">
                <a href="#" class="dropdown-item">{{ key }}</a>
                {% endfor %}
            </div>
        </div>
    </div>
</div>
</section>
{% endblock %}

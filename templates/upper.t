<!DOCTYPE html>
<html lang="{{ html_lang_setting }}">
<head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <title>{{ head_title }}</title>
    <link rel="stylesheet" href="/css/bulma.min.css">
    <link rel="shortcut icon" type="image/x-icon" href="/css/favicon.ico" />
</head>
<body>
<section class="hero has-background-info-light">
  <div class="hero-body pt-4">
    <nav class="level">
  <!-- Left side -->
<div class="level-left">
{% block logo %}
{% if languages == 1 %}
<span class="tag is-danger"><strong>Testing pågår</strong></span> <!-- only norsk -->
<!--<span class="tag is-warning"><strong>BETA versjon</strong></span> -->
{% else %}
<div class="dropdown is-hoverable is-primary">
  <div class="dropdown-trigger">
    <button class="button has-icons-right" aria-haspopup="true" aria-controls="dropdown-menu3">
      <span>{{ lang_selector }}</span>
    </button>
  </div>
  <div class="dropdown-menu" id="dropdown-menu3" role="menu">
    <div class="dropdown-content">
      {% for lang in html_lang %}
      <a href="/lang/{{lang}}"" class="dropdown-item">
        {{lang}}
      </a>
      {% endfor %}
    </div>
  </div>
</div>
{% endif %}
{% endblock %}
</div>

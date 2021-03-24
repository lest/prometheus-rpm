{% block environment -%}
{%- for key, value in environment.items() -%}
{{ key|upper }}="{{ value }}"
{% endfor -%}
{{ name|upper }}_OPTS="{{ service_opts|join(' ') }}"
{% endblock environment %}

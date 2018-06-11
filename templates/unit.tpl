# -*- mode: conf -*-

[Unit]
{% block unit %}
Description=P{{description}}
Documentation={{URL}}
After=network.target
{% endblock unit %}

[Service]
{% block service %}
EnvironmentFile=-/etc/default/{{name}}
User=prometheus
ExecStart=/usr/bin/{{name}} ${{name|upper}}_EXPORTER_OPTS
Restart=on-failure
{% endblock service %}

[Install]
{% block install %}
WantedBy=multi-user.target
{% endblock install %}
# -*- mode: conf -*-

[Unit]
{% block unit %}
Description={{summary}}
Documentation={{URL}}
After=network.target
{% endblock unit %}

[Service]
{% block service %}
EnvironmentFile=-/etc/default/{{name}}
User={{user}}
ExecStart=/usr/bin/{{name}} ${{name|upper}}_OPTS
Restart=on-failure
RestartSec=5s
{% endblock service %}

[Install]
{% block install %}
WantedBy=multi-user.target
{% endblock install %}

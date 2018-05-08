# -*- mode: conf -*-

[Unit]
Description={{summary}}
Documentation={{URL}}
After=network.target

[Service]
EnvironmentFile=-/etc/default/{{name}}
User=prometheus
ExecStart=/usr/bin/{{name}} ${{name|upper}}_OPTS
Restart=on-failure

[Install]
WantedBy=multi-user.target

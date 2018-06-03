# -*- mode: conf -*-

[Unit]
Description=P{{description}}
Documentation={{URL}}
After=network.target

[Service]
EnvironmentFile=-/etc/default/{{name}}
User=prometheus
ExecStart=/usr/bin/{{name}} ${{name}}_EXPORTER_OPTS
Restart=on-failure

[Install]
WantedBy=multi-user.target
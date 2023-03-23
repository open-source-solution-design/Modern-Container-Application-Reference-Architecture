#!/bin/sh
/usr/bin/prometheus --config.file=/etc/prometheus/prometheus.yml --web.listen-address="0.0.0.0:9091" --web.enable-lifecycle --enable-feature=agent --storage.agent.path="/opt/prometheus/data-agent/"

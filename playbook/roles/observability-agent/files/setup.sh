#!/bin/bash
set -x
export observableserver=$1
export port=$2
export deepflowserverip=$3
export deepflowserverid=$4

cat > values.yaml << EOF
kube-state-metrics:
  enabled: false
prometheus-to-cloudwatch:
  enabled: false
deepflow-agent:
  enabled: true
  deepflowServerNodeIPS:
    - $deepflowserverip
  deepflowK8sClusterID: $deepflowserverid
prometheus:
  enabled: true
  server:
    extraFlags:
    - enable-feature=expand-external-labels
    remoteWrite:
    - name: remote_prometheus
      url: 'https://${obserableserver}:${port}/api/v1/write'
  alertmanager:
    enabled: false
  rometheus-pushgateway:
    enabled: false
fluent-bit:
  enabled: true
  logLevel: debug
  config:
    outputs: |
      [OUTPUT]
          Name        loki
          Match       kube.*
          Host        $obserableserver
          port        $port
          tls         on
          tls.verify  on
EOF

helm repo add stable https://artifact.onwalk.net/chartrepo/k8s/
helm repo update
helm upgrade --install observableagent stable/observableagent -n monitoring --create-namespace -f values.yaml

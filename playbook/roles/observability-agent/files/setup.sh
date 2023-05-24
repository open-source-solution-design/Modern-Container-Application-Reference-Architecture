#!/bin/bash
set -x
export observableserver=$1
export port=$2
export deepflowserverip=$3
export deepflowserverid=$4

cat > values.yaml << EOF
kube-state-metrics:
  enabled: true
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
    - web.enable-lifecycle
    remoteWrite:
    - name: remote_prometheus
      url: 'https://${obserableserver}/api/v1/write'
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

node_name=`kubectl get nodes | awk 'NR>1 {print $1}'`
kubectl create namespace monitoring || echo true
kubectl label nodes $node prometheus=true --overwrite || echo true
helm repo add stable https://artifact.onwalk.net/chartrepo/public/ || echo true
helm repo update
helm upgrade --install observableagent stable/observabilityagent -n monitoring -f values.yaml

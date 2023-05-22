#!/bin/bash

export token=$1

helm repo add datadog https://helm.datadoghq.com
helm repo update
cat > datadog-values.yaml << EOF
#registry: artifact.onwalk.net/public/datadog
targetSystem: "linux"
clusterAgent:
  enabled: true
  admissionController:
    enabled: true
    mutateUnlabelled: true
datadog:
  site: 'datadoghq.eu'
  apiKeyExistingSecret: datadog-agent
  apm:
    portEnabled: true
  networkMonitoring:
    enabled: false
  logs:
    enabled: false
    containerCollectAll: false
EOF
kubectl create namespace datadog || echo true
kubectl delete secret datadog-agent --namespace=datadog || echo true
kubectl create secret generic datadog-agent --from-literal api-key=$token --namespace=datadog
helm upgrade --install datadog-agent -n datadog --create-namespace -f datadog-values.yaml datadog/datadog

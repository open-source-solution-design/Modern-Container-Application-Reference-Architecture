#!/bin/bash

domain=$1
namespace=$2
gitlab_secret=$4

cat > gitlab-values.yaml <<EOF
global:
  edition: ce
  hosts:
    https: true
    domain: $domain
    gitlab:
      name: gitlab.$domain
  ingress:
    class: nginx
    enabled: true
    configureCertmanager: false
    tls:
      enabled: true
      secretName: ${gitlab_secret}
  minio:
    enabled: true
  appConfig:
    omniauth:
      enabled: true
registry:
  enabled: true
  ingress:
    enabled: false
gitlab-exporter:
  enabled: false
kas:
  enabled: false
nginx-ingress:
  enabled: false
prometheus:
  install: false
redis:
  metrics:
    enabled: false
postgresql:
  metrics:
    enabled: false
certmanager:
  install: false
  installCRDs: false
  startupapicheck:
    enabled: false
upgradeCheck:
  enabled: false
EOF

export KUBECONFIG=/etc/rancher/k3s/k3s.yaml
helm repo add gitlab https://charts.gitlab.io/
helm repo up
kubectl create namespace gitlab || true
helm upgrade --install gitlab gitlab/gitlab --version=6.6.1 --namespace gitlab -f gitlab-values.yaml

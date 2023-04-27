#!/bin/bash

domain=$1
namespace=$2
gitlab_secret=$3
gitlab_sso_secret=$4

cat > gitlab-values.yaml <<EOF
global:
  edition: ce
  hosts:
    domain: $domain
    gitlab:
      name: gitlab.$domain
    https: true
  ingress:
    class: nginx
    configureCertmanager: false
    enabled: true
    tls:
      enabled: true
      secretName: $gitlab_secret
  minio:
    enabled: true
  appConfig:
    omniauth:
      enabled: true
      autoLinkLdapUser: false
      autoLinkSamlUser: false
      blockAutoCreatedUsers: false
      autoSignInWithProvider: null
      autoLinkUser:
        - 'openid_connect'
      allowSingleSignOn:
        - 'openid_connect'
      providers:
      - secret: $gitlab_sso_secret
        key: provider
kas:
  enabled: false
nginx-ingress:
  enabled: false
postgresql:
  metrics:
    enabled: false
prometheus:
  install: false
redis:
  metrics:
    enabled: false
upgradeCheck:
  enabled: false
certmanager:
  install: false
  installCRDs: false
  startupapicheck:
    enabled: false
gitlab-exporter:
  enabled: false
EOF

export KUBECONFIG=/etc/rancher/k3s/k3s.yaml
helm repo add gitlab https://charts.gitlab.io/
helm repo up
kubectl create namespace gitlab || true
helm upgrade --install gitlab gitlab/gitlab --version=6.6.1 --namespace gitlab -f gitlab-values.yaml

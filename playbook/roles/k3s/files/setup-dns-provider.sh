#!/bin/bash

ak=$1
sk=$2

cat > external-dns-values.yaml << EOF
clusterDomain: admin.local
sources:
  - service
  - ingress
domainFilters:
  - onwalk.net
policy: upsert-only
provider: alibabacloud
alibabacloud:
  accessKeyId: $ak
  accessKeySecret: $sk
  regionId: rg-acfm2akhd255pgi
  zoneType: public
EOF

export KUBECONFIG=/etc/rancher/k3s/k3s.yaml
sudo helm repo add bitnami https://charts.bitnami.com/bitnami || echo true
sudo helm repo update
sudo kubectl create namespace external-dns || echo true
sudo helm upgrade --install external-dns -f external-dns-values.yaml bitnami/external-dns -n external-dns

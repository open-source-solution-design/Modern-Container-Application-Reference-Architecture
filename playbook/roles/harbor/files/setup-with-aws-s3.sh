#!/bin/bash

ak=$1
sk=$2
domain=$3
namespace=$4
secret_name=$5

cat > harbor-config.yaml << EOF
expose:
  type: ingress
  tls:
    enabled: true
    certSource: secret
    secret:
      secretName: $secret_name
      notarySecretName: $secret_name
  ingress:
    hosts:
      core: artifact.${domain}
      notary: notary.${domain}
    className: "nginx"
persistence:
  imageChartStorage:
    type: s3
    s3:
      region: cn-northwest-1
      bucket: apollo-artifact
      accesskey: $ak
      secretkey: $sk
externalURL: https://artifact.${domain}
EOF

export KUBECONFIG=/etc/rancher/k3s/k3s.yaml
helm repo add harbor https://helm.goharbor.io
helm repo update
helm upgrade --install artifact harbor/harbor -f harbor-config.yaml -n $namespace

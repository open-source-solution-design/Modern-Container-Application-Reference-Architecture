#!/bin/bash

domain=$1
ak=$2
sk=$3

cat > harbor-config.yaml << EOF
expose:
  type: ingress
  tls:
    enabled: true
    certSource: secret
    secret:
      secretName: "harbor-tls"
      notarySecretName: "harbor-tls"
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
kubectl create namespace artifact
kubectl delete secret harbor-tls -n artifact
kubectl create secret tls harbor-tls --cert=/etc/ssl/${domain}.pem --key=/etc/ssl/${domain}.key -n artifact
helm repo add harbor https://helm.goharbor.io
helm repo update
helm upgrade --install artifact harbor/harbor -f harbor-config.yaml -n artifact

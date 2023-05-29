#!/bin/bash

export domain=$1
export secret=$2
export namespace=$3
export keycloak_ui_password=$4
export keycloak_db_password=$5

cat > keycloak-values.yaml << EOF
postgresql:
  enabled: false
ingress:
  enabled: true
  ingressClassName: "nginx"
  hostname: keycloak.${domain}
  tls: true
  extraTls:
  - hosts:
      - keycloak.${domain}
    secretName: $secret
auth:
  adminPassword: "$keycloak_ui_password"
externalDatabase:
  host: "postgresql.database.svc.cluster.local"
  port: 5432
  user: postgres
  database: keycloak
  password: "$keycloak_db_password"
EOF

helm repo add bitnami https://charts.bitnami.com/bitnami || echo true
helm repo add stable https://artifact.onwalk.net/chartrepo/public/ || echo true
helm repo update
kubectl create ns ${namespace} || echo true
helm upgrade --install keycloak bitnami/keycloak -n $namespace -f keycloak-values.yaml

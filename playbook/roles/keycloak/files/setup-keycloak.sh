#!/bin/bash

export keycloak_db_password=$1
export keycloak_ui_password=$2
export domain=$3
export secret=$4
export namespace=$5

cat > keycloak-vaules.yaml << EOF
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
  user: keycloak
  database: keycloak
  password: "$keycloak_db_password"
EOF

helm repo add bitnami https://charts.bitnami.com/bitnami
helm repo update
helm upgrade --install keycloak bitnami/keycloak -n $namespace -f keycloak-vaules.yaml

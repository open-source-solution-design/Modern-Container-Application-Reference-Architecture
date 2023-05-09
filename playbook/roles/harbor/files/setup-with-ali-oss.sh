#!/bin/bash

ak=$1
sk=$2
domain=$3
namespace=$4
secret_name=$5
redis_passwd=$6
pg_db_password=$7

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
      core: harbor.${domain}
      notary: notary.${domain}
    className: "nginx"
database:
  type: external
  external:
    host: "postgresql.database.svc.cluster.local"
    port: "5432"
    username: "user"
    password: "$pg_db_password"
    coreDatabase: "registry"
    notaryServerDatabase: "notary_server"
    notarySignerDatabase: "notary_signer"
redis:
  type: external
  external:
    addr: "redis-master.redis.svc.cluster.local:6379"
#    password: "$redis_password"
persistence:
  imageChartStorage:
    type: oss
    oss:
      accesskeyid: $ak
      accesskeysecret: $sk
      region: "oss-cn-wulanchabu"
      bucket: "harbor-s3"
      endpoint: "oss-cn-wulanchabu.aliyuncs.com"
externalURL: https://harbor.${domain}
EOF

export KUBECONFIG=/etc/rancher/k3s/k3s.yaml
helm repo add harbor https://helm.goharbor.io
helm repo update
helm upgrade --install artifact harbor/harbor -f harbor-config.yaml -n $namespace

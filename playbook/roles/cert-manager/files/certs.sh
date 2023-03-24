#!/bin/bash

export Ali_Key=$1
export Ali_Secret=$2
export domain=$3
export secret=$4
export namespace=$5

curl https://get.acme.sh | sh -s email=156405189@qq.com

rm -rvf ${domain}.* -f
sh ~/.acme.sh/acme.sh --set-default-ca --server zerossl --issue --force --dns dns_ali -d ${domain} -d "*.${domain}"
cat ~/.acme.sh/${domain}/${domain}.cer > ${domain}.pem
cat ~/.acme.sh/${domain}/ca.cer >> ${domain}.pem
cat ~/.acme.sh/${domain}/${domain}.key > ${domain}.key

kubectl create namespace $namespace || echo true
kubectl delete secret tls $secret -n $namespace || echo true
kubectl create secret tls $secret --cert=${domain}.pem --key=${domain}.key -n $namespace

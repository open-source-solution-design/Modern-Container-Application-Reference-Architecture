#!/bin/bash
set -x
export domain=$1
export Ali_Key=$2
export Ali_Secret=$3

curl https://get.acme.sh | sh -s email=156405189@qq.com

rm -rvf ${domain}.* -f
sh ~/.acme.sh/acme.sh --set-default-ca --server google --issue --force --dns dns_ali -d ${domain} -d "*.${domain}"
cat ~/.acme.sh/${domain}_ecc/${domain}.cer > ${domain}.pem
cat ~/.acme.sh/${domain}_ecc/ca.cer >> ${domain}.pem
cat ~/.acme.sh/${domain}_ecc/${domain}.key > ${domain}.key
sudo cp ${domain}.pem /etc/ssl/
sudo cp ${domain}.key /etc/ssl/

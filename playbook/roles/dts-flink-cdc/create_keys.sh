#!/bin/bash

export name=$1
export server_key=$2
export server_ip=$3
export client_ip=$4

sudo rm -rvf /etc/wireguard/keys/$name
sudo mkdir -pv /etc/wireguard/keys/$name
cd  /etc/wireguard/keys/$name
wg genkey > ${name}.key
wg pubkey < ${name}.key > ${name}.pub

KEY=`cat ${name}.key`
PUBKEY=`cat ${name}.pub`

cat > ${name}-wg0.conf << EOF
[Interface]
PrivateKey = ${KEY}
ListenPort = 54321
Address = ${client_ip}/24
DNS = 10.1.0.2, 114.114.114.114
MTU = 1420
[Peer]
PublicKey = ${server_key}
AllowedIPs = 10.255.0.0/24, 10.1.0.0/16
Endpoint = ${server_ip}:51820
PersistentKeepalive = 25
EOF


# brew install wireguard-tools && sudo wg-quick up wg0
# apt install qrencode --assume-yes qrencode --read-from=client-wg0.conf --type=UTF8

cat >> /etc/wireguard/wg0.conf << EOF
[Peer]
   # ${name}
   PublicKey = ${PUBKEY}
   AllowedIPs = ${client_ip}/32
EOF

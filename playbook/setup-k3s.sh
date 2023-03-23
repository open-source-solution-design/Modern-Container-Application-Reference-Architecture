#!/bin/bash

dns_ak=`printenv DNS_AK`
dns_sk= `printenv DNS_SK`
ssh_private_key=`printenv SSH_PRIVATE_KEY`
db_server_public_ip=`pulumi stack output --json | jq '.db_server_public_ip'`
k3s_server_public_ip=`pulumi stack output --json | jq '.k3s_server_public_ip'`

cat > hosts/id_rsa << EOF
$ssh_private_key
EOF

sudo chmod 0400 hosts/id_rsa

cat > hosts/inventory << EOF
[master]
k3s-server               ansible_host=$k3s_server_public_ip

[node]
db-server                ansible_host=$db_server_public_ip

[all:vars]
ansible_port=22
ansible_ssh_user=ubuntu
ansible_ssh_private_key_file=hosts/id_rsa
ansible_host_key_checking=False
dns_ak=$dns_ak
dns_sk=$dns_sk
lb_ip=$k3s_server_ip
EOF

ansible-playbook -i hosts/inventory jobs/init_k3s_cluster -D
ansible-playbook -i hosts/inventory jobs/init_monitor -D
ansible-playbook -i hosts/inventory jobs/init_log_agent -D


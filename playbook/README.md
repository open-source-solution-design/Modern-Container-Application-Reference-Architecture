# playbook

# Getting started

## Delpoy Test
ansible-playbook -i hosts/aws-hosts jobs/init_ec2_monitoring -D -C
ansible-playbook -i hosts/aws-hosts jobs/init_ec2_monitoring_sit -D -C
ansible-playbook -i hosts/aws-hosts jobs/init_ec2_monitoring_uat -D -C
ansible-playbook -i hosts/aws-hosts jobs/init_ec2_monitoring_common -D -C

## Deploy

ansible-playbook -i hosts/aws-hosts jobs/init_ec2_monitoring -D
ansible-playbook -i hosts/aws-hosts jobs/init_ec2_monitoring_sit -D
ansible-playbook -i hosts/aws-hosts jobs/init_ec2_monitoring_uat -D
ansible-playbook -i hosts/aws-hosts jobs/init_ec2_monitoring_common -D

## Troubleshooting

ansible -i  hosts/aws-hosts sit -m shell -a 'sudo pkill -9 prometheus'

"""An AWS Python Pulumi AWS Module"""
import aws
import config
import pulumi

vpc_id  = aws.vpc()
az_list = aws.availability_zones()
sg_id   = aws.security_group( vpc_id )
igw_id  = aws.internet_gateway( vpc_id )
route_table_id = aws.route_table( vpc_id, igw_id )
subnets = aws.subnets(vpc_id, az_list, route_table_id, 'public' )

ssh_key  = config.get_env('SSH_PUBLIC_KEY')
key_pair = aws.key_pair(resource_name="my_ssh_key", public_key=ssh_key)

k3s_server = aws.ec2(
        arch      = 'amd64',
        ec2_name  = 'webui.onwalk.net',
        ec2_type  = 't3.large',
        key_name  = key_pair,
        subnet_id = subnet_id,
        secuity_group_id = sg_id
        )
db_server = aws.ec2(
        arch      = 'arm64',
        ec2_name  = 'clickhouse.onwalk.net',
        ec2_type  = 't4g.medium',
        key_name  = key_pair,
        subnet_id = subnet_id,
        secuity_group_id = sg_id
        )

pulumi.export("vpc", vpc_id)
pulumi.export("sg", sg_id)
pulumi.export("subnets", subnets)
pulumi.export("key_pair", key_pair)
pulumi.export("k3s_server_public_ip", k3s_server.public_ip )
pulumi.export("db_server_public_ip",  db_server.public_ip )

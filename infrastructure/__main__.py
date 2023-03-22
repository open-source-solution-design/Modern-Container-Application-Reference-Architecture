"""An AWS Python Pulumi AWS Module"""
from aws import vpc
from aws import subnets
from aws import route_table
from aws import security_group
from aws import internet_gateway
from aws import availability_zones
from aws import key_pair
from aws import ec2

from pulumi import export
from config import get_env

vpc_id  = vpc()
az_list = availability_zones()
sg_id   = security_group( vpc_id )
igw_id  = internet_gateway( vpc_id )
route_table_id = route_table( vpc_id, igw_id )
subnets = subnets(vpc_id, az_list, route_table_id, 'public' )

ssh_key  = get_env('SSH_PUBLIC_KEY')
key_pair = key_pair(resource_name="my_ssh_key", public_key=ssh_key)

k3s_server = ec2(
        arch      = 'amd64',
        ec2_name  = 'webui.onwalk.net',
        ec2_type  = 't3.large',
        key_name  = key_pair,
        subnet_id = subnet_id,
        secuity_group_id = sg_id
        )
db_server = ec2(
        arch      = 'arm64',
        ec2_name  = 'clickhouse.onwalk.net',
        ec2_type  = 't4g.medium',
        key_name  = key_pair,
        subnet_id = subnet_id,
        secuity_group_id = sg_id
        )

export("vpc", vpc_id)
export("sg", sg_id)
export("subnets", subnets)
export("key_pair", key_pair)
export("k3s_server_public_ip", k3s_server.public_ip )
export("db_server_public_ip",  db_server.public_ip )

"""An AWS Python Pulumi AWS Module"""
import config
import pulumi

from aws import vpc
from aws import subnets
from aws import route_table
from aws import security_group
from aws import internet_gateway
from aws import availability_zones
from aws import key_pair

vpc_id  = vpc()
az_list = availability_zones()
sg_id   = security_group( vpc_id )
igw_id  = internet_gateway( vpc_id )
route_table_id = route_table( vpc_id, igw_id )
subnets = subnets(vpc_id, az_list, route_table_id, 'public' )

from pulumi_command import local

def get_env( name ):
    result = local.Command(
            "command",
            create=f'printenv {name}'
            )
    return result.stdout

ssh_public_key=get_env('SSH_PUBLIC_KEY')
pulumi.export("ssh_public_key", ssh_public_key)

key_pair_name = key_pair(
        "my_ssh_key",
        public_key=config.get_env('SSH_PUBLIC_KEY')
    )

pulumi.export("vpc", vpc_id)
pulumi.export("sg", sg_id)
pulumi.export("subnets", subnets)
pulumi.export("keypair", key_pair_name)

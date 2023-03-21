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

from pulumi_command import local

vpc_id  = vpc()
az_list = availability_zones()
sg_id   = security_group( vpc_id )
igw_id  = internet_gateway( vpc_id )
route_table_id = route_table( vpc_id, igw_id )
subnets = subnets(vpc_id, az_list, route_table_id, 'public' )

ssh_key = local.Command("random",
    create="env | grep SSH_PUBLIC_KEY | awk -F= '{print $2}'"
)

pulumi.export("sshkey", key.stdout)

key_pair = pulumi.aws.ec2.KeyPair("deployer", public_key=ssh_key)

# Create an AWS resource (S3 Bucket)
#bucket = s3.Bucket('my-bucket')

# Export the name of the bucket
pulumi.export('bucket_name', bucket)
pulumi.export("vpc", vpc_id)
pulumi.export("sg", sg_id)
pulumi.export("subnets", subnets)
pulumi.export("keypair", key_pair.key_name)

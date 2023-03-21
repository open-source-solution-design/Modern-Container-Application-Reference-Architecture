import pulumi
from pulumi_aws import s3, ec2, get_availability_zones

stack_name = pulumi.get_stack()
project_name = pulumi.get_project()
config = pulumi.Config('aws')

#------------------------------------#
def vpc():
    vpc = ec2.Vpc(resource_name=f"eks-{project_name}-{stack_name}",
              cidr_block="10.100.0.0/16",
              enable_dns_support=True,
              enable_dns_hostnames=True,
              instance_tenancy='default',
              tags={"Project": project_name,
                    "Stack": stack_name})
    return vpc.id

#------------------------------------#
def key_pair( key_pair_name, config_key_name ):
    ssh_public_key = config.require( config_key_name )
    keypair = ec2.KeyPair( key_pair_name, ssh_public_key)
    return keypair.key_name
#------------------------------------#
def availability_zones():
    """Use availability zones defined in the configuration file if available"""
    if config.get('az_list'):
        az_list = config.get_object('az_list')
    else:
        az_list = get_availability_zones(state="available").names
  
    return az_list

#------------------------------------#
def internet_gateway( vpc_id ):
    igw = ec2.InternetGateway(
            resource_name=f'vpc-ig-{project_name}-{stack_name}',
            vpc_id=vpc_id,
            tags={
                "Project": project_name,
                "Stack": stack_name
                }
            )
    return igw.id

#------------------------------------#
def route_table( vpc_id, igw_id ):
    route_table = ec2.RouteTable(
            resource_name=f'vpc-route-table-{project_name}-{stack_name}',
            vpc_id=vpc_id,
            routes=[ec2.RouteTableRouteArgs(
                cidr_block='0.0.0.0/0',
                gateway_id=igw_id)
                    ],
            tags={
                "Project": project_name,
                "Stack": stack_name
                }
            )
    return route_table.id

#------------------------------------#
def security_group( vpc_id ):
    security_group = ec2.SecurityGroup(
            resource_name=f'ec2-sg-{project_name}-{stack_name}',
            vpc_id=vpc_id,
            description="Allow all HTTP(s) traffic to EKS Cluster",
            ingress=[
                ec2.SecurityGroupIngressArgs(
                    protocol='tcp',
                    from_port=22,
                    to_port=22,
                    cidr_blocks=['0.0.0.0/0'],
                    description='Allow sshd connect'),
                ec2.SecurityGroupIngressArgs(
                    protocol='tcp',
                    from_port=443,
                    to_port=443,
                    cidr_blocks=['0.0.0.0/0'],
                    description='Allow https 443'),
                ec2.SecurityGroupIngressArgs(
                    protocol='tcp',
                    from_port=80,
                    to_port=80,
                    cidr_blocks=['0.0.0.0/0'],
                    description='Allow http 80')
                   ],
            tags={
                "Project": project_name,
                "Stack": stack_name
                }
            )
    return security_group.id

#------------------------------------#
def subnets( vpc_id, az_name, route_table_id, net_type='private' ):

# If you wanted to double the number of subnets because you have few
# availability zones, you can redefine the variable below to something
# like: list(itertools.chain(azs, azs)) which would just repeat the
# same list of AZs twice. The iteration logic will pick it up for
# subnet creation and create unique names.

    subnets = []

    if config.get('az_list'):
        az_list = config.get_object('az_list')
    else:
        az_list = get_availability_zones(state="available").names

    az_enum = list(az_list)

    if len(az_list) <= 0:
        raise ValueError("There are no usable availability zones")
    if len(az_list) == 1:
        pulumi.log.warn("There is only a single usable availability zone")
    elif len(az_list) == 2:
        pulumi.log.warn("There are only two usable availability zones")
    
    for i, az in enumerate(az_enum):
        
        if net_type == 'public':
            subnet_addr = i
            map_eip=True
        if net_type == 'private':
            subnet_addr = (i + 1) * 16
            map_eip=False

        if not isinstance(az, str):
            raise f'availability zone specified [{i}] is not a valid string value: [{az}]'
        if az.strip() == "":
            raise f'availability zone specified [{i}] is an empty string'
    
        subnet = ec2.Subnet(
                resource_name = f'{az}-{net_type}-{project_name}-{stack_name}-{i}',
                vpc_id=vpc_id,
                availability_zone=az,
                cidr_block=f"10.100.{subnet_addr}.0/24",
                map_public_ip_on_launch=map_eip,
                tags={
                    "Project": project_name,
                    "Stack": stack_name,
                    }
                )
        ec2.RouteTableAssociation(
                f"route-table-assoc-{net_type}-{az}-{i}",
                route_table_id=route_table_id,
                subnet_id=subnet.id
                )
        subnets.append(subnet.id)
    
    return subnets

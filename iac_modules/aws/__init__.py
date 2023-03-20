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
    return vpc

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

#------------------------------------#
def route_table( vpc_id, igw_id ):
    route_table = ec2.RouteTable(
            resource_name=f'vpc-route-table-{project_name}-{stack_name}',
            vpc_id=vpc_id,
            routes=[ec2.RouteTableRouteArgs(
                cidr_block='0.0.0.0/0',
                gateway_id=igw.id)
                    ],
            tags={
                "Project": project_name,
                "Stack": stack_name
                }
            )

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
    return security_group 

#------------------------------------#
def subnets( vpc_id, az_name, route_table_id, net_type='private' ):

    subnets = []

# If you wanted to double the number of subnets because you have few
# availability zones, you can redefine the variable below to something
# like: list(itertools.chain(azs, azs)) which would just repeat the
# same list of AZs twice. The iteration logic will pick it up for
# subnet creation and create unique names.

    if config.get('az_list'):
        az_list = config.get_object('az_list')
    else:
        az_list = get_availability_zones(state="available").names

    replica = list(az_list)

    if len(replica) <= 0:
        raise ValueError("There are no usable availability zones")
    if len(replica) == 1:
        pulumi.log.warn("There is only a single usable availability zone")
    elif len(replica) == 2:
        pulumi.log.warn("There are only two usable availability zones")
    
    for i, az_list in enumerate(replica):
        
        if net_type ==public:
            subnet_addr = i
            map_eip=True
        if net_type ==private:
            subnet_addr = (i + 1) * 16
            map_eip=False

        if not isinstance(az_list, str):
            raise f'availability zone specified [{i}] is not a valid string value: [{az_list}]'
        if az_list.strip() == "":
            raise f'availability zone specified [{i}] is an empty string'
    
        resource_name = f'{az}-k8s-{net_type}-{project_name}-{stack_name}-{i}'
        subnet = ec2.Subnet(resource_name=resource_name,
                            availability_zone=az_name,
                            vpc_id=vpc_id,
                            cidr_block=f"10.100.{subnet_addr}.0/24",
                            map_public_ip_on_launch=map_eip,
                            tags={"Project": project_name,
                                  "Stack": stack_name,
                                  "kubernetes.io/role/elb": "1"})
        ec2.RouteTableAssociation(f"route-table-assoc-{net_type}-{az}-{i}",
                                  route_table_id=route_table_id,
                                  subnet_id=subnet.id)
        subnets.append(subnet)
    
    return subnets

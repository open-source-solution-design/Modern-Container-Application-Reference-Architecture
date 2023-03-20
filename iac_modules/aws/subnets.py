def subnets( vpc_id, az_name, route_table_id, net_type=private ):

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

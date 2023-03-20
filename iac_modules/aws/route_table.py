def route_table( igw_id ):
    route_table = ec2.RouteTable(
            resource_name=f'vpc-route-table-{project_name}-{stack_name}',
            vpc_id=vpc.id,
            routes=[ec2.RouteTableRouteArgs(
                cidr_block='0.0.0.0/0',
                gateway_id=igw.id)
                    ],
            tags={
                "Project": project_name,
                "Stack": stack_name
                }
            )

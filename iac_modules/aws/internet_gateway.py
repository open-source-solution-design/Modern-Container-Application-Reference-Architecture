def internet_gateway():
    igw = ec2.InternetGateway(
            resource_name=f'vpc-ig-{project_name}-{stack_name}',
            vpc_id=vpc.id,
            tags={
                "Project": project_name,
                "Stack": stack_name
                }
            )

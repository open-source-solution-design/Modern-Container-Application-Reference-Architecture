def security_group( vpc_id ):
    security_group = ec2.SecurityGroup(
            resource_name=f'ec2-sg-{project_name}-{stack_name}',
            vpc_id=vpc.id,
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
                   ]
            tags={
                "Project": project_name,
                "Stack": stack_name
                }
            )
    return secrity_group

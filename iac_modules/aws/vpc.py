def vpc():
    vpc = ec2.Vpc(resource_name=f"eks-{project_name}-{stack_name}",
              cidr_block="10.100.0.0/16",
              enable_dns_support=True,
              enable_dns_hostnames=True,
              instance_tenancy='default',
              tags={"Project": project_name,
                    "Stack": stack_name})
    return vpc

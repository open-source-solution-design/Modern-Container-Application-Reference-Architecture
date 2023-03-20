import pulumi
import pulumi_aws

stack_name = pulumi.get_stack()
project_name = pulumi.get_project()

config = pulumi.Config('aws')

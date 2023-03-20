import pulumi
from pulumi_aws import s3, ec2, get_availability_zones

stack_name = pulumi.get_stack()
project_name = pulumi.get_project()

config = pulumi.Config('aws')

print("You have imported mypackage")

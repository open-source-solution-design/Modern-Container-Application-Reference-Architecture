"""An AWS Python Pulumi AWS Module"""

import aws

vpc = aws.vpc()
igw = aws.internet_gateway()
az_list = aws.availability_zones()
sg = security_group(vpc_id=vpc.id )
route_table = route_table( igw.id )

subnets=subnets(vpc_id=vpc.id, az_name=az_list, route_table_id=route_table.id, net_type=public )


# Create an AWS resource (S3 Bucket)
bucket = s3.Bucket('my-bucket')

# Export the name of the bucket
pulumi.export('bucket_name', bucket.id)
pulumi.export("vpc", vpc.id)
pulumi.export("sg", sg.id)
pulumi.export("subnets", subnets)

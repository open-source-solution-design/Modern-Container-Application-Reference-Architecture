"""An AWS Python Pulumi AWS Module"""

import aws

vpc_id = aws.vpc()
sg_id = aws.security_group(vpc_id )
az_list = aws.availability_zones()
igw_id = aws.internet_gateway( vpc_id )
route_table_id = aws.route_table( vpc_id, igw_id )

subnets=subnets(vpc_id=vpc_id, az_name=az_list, route_table_id=route_table_id, net_type=public )


# Create an AWS resource (S3 Bucket)
bucket = s3.Bucket('my-bucket')

# Export the name of the bucket
pulumi.export('bucket_name', bucket)
pulumi.export("vpc", vpc_id)
pulumi.export("sg", sg_id)
pulumi.export("subnets", subnets)

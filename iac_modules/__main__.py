"""An AWS Python Pulumi AWS Module"""

from aws import vpc, security_group, availability_zones, internet_gateway, route_table, subnets 

vpc_id  = vpc()
sg_id   = security_group( vpc_id )
az_list = availability_zones()
igw_id  = internet_gateway( vpc_id )
route_table_id = route_table( vpc_id, igw_id )

subnets=subnets(vpc_id, az_list, route_table_id, 'public' )

# Create an AWS resource (S3 Bucket)
#bucket = s3.Bucket('my-bucket')

# Export the name of the bucket
pulumi.export('bucket_name', bucket)
pulumi.export("vpc", vpc_id)
pulumi.export("sg", sg_id)
pulumi.export("subnets", subnets)

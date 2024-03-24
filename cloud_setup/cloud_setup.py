import boto3

# Initialize clients using boto3
ec2_resource = boto3.resource('ec2', region_name='us-east-1')
ec2_client = boto3.client('ec2', region_name='us-east-1')
iam_client = boto3.client('iam')
elasticache_client = boto3.client('elasticache', region_name='us-east-1')

def create_ec2_instance(security_group_id, key_name):
    instance = ec2_resource.create_instances(
        ImageId='ami-0d7a109bf30624c99', 
        MinCount=1,
        MaxCount=1,
        InstanceType='t2.micro',
        KeyName=key_name,
        SecurityGroupIds=[security_group_id],
        TagSpecifications=[{'ResourceType': 'instance', 'Tags': [{'Key': 'Name', 'Value': 'FlaskAppServer'}]}],
    )
    print(f"EC2 Instance created: {instance[0].id}")
    return instance[0].id

def create_security_group():
    response = ec2_client.create_security_group(GroupName='FlaskAppSG', Description='SG for Flask App')
    security_group_id = response['GroupId']
    print(f'Security Group Created {security_group_id}.')

    data = ec2_client.authorize_security_group_ingress(
        GroupId=security_group_id,
        IpPermissions=[{'IpProtocol': 'tcp', 'FromPort': 80, 'ToPort': 80, 'IpRanges': [{'CidrIp': '0.0.0.0/0'}]},
                       {'IpProtocol': 'tcp', 'FromPort': 22, 'ToPort': 22, 'IpRanges': [{'CidrIp': '0.0.0.0/0'}]}])
    print('Ingress Successfully Set.')
    return security_group_id


def create_elasticache_redis():
    try:
        response = elasticache_client.create_replication_group(
            ReplicationGroupId='my-redis-cluster',
            ReplicationGroupDescription='Redis cluster for my application',
            NumNodeGroups=1,
            AutomaticFailoverEnabled=False,
            CacheNodeType='cache.t2.micro',
            Engine='redis',
            EngineVersion='6.x',
            CacheParameterGroupName='default.redis6.x',
            NumCacheClusters=1,
        )
        print("ElastiCache Redis cluster creation initiated.")
    except Exception as e:
        print(f"Failed to create ElastiCache Redis cluster: {e}")

if __name__ == "__main__":
    # Creates Security Group
    sg_id = create_security_group()
    
    # Creates EC2 Instance
    ec2_id = create_ec2_instance(sg_id, 'ClickCounter')  # Ensure your key pair is created in advance
    
    # Creates ElastiCache Redis
    create_elasticache_redis()

    print("Infrastructure setup complete.")

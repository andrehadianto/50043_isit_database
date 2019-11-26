import boto3
from botocore.exceptions import ClientError, WaiterError

def create_ec2_instance(image_id, instance_type, keypair_name, security_group, script_path=None):

    # Provision and launch the EC2 instance
    ec2_client = boto3.client(
        'ec2')

    try:
        if script_path != None:
            with open(script_path, 'r') as f:
                script = '\n'.join(f)
                response = ec2_client.run_instances(ImageId=image_id,
                                                    InstanceType=instance_type,
                                                    KeyName=keypair_name,
                                                    MinCount=1,
                                                    MaxCount=1,
                                                    SecurityGroups=security_group,
                                                    UserData=script)
        else:
            response = ec2_client.run_instances(ImageId=image_id,
                                                    InstanceType=instance_type,
                                                    KeyName=keypair_name,
                                                    MinCount=1,
                                                    MaxCount=1,
                                                    SecurityGroups=security_group)
                                            

        instanceId = response['Instances'][0]["InstanceId"]

        try:
            ec2_client.get_waiter('instance_running').wait(InstanceIds=[instanceId])
            response_final = ec2_client.describe_instances(InstanceIds=[instanceId])
    
        except WaiterError as e:
            logging.error(e)

    except ClientError as e:
        logging.error(e)
        return None
    
    return response_final['Reservations'][0]['Instances'][0]


def create_security_group(name, permissions):    
    ec2 = boto3.client('ec2')

    response = ec2.describe_vpcs()
    vpc_id = response.get('Vpcs', [{}])[0].get('VpcId', '')

    try:
        response = ec2.create_security_group(GroupName=name,
                                            Description="DESCRIPTION",
                                            VpcId=vpc_id)
        security_group_id = response['GroupId']
        print('Security Group Created %s in vpc %s.' % (security_group_id, vpc_id))

        data = ec2.authorize_security_group_ingress(
            GroupId=security_group_id,
            IpPermissions=permissions)
        print('Ingress Successfully Set %s' % data)

    except ClientError as e:
        print(e)

    return security_group_id
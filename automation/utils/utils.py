from botocore.exceptions import ClientError, WaiterError
import boto3
import paramiko
import time
import utils.user


def create_ec2_instance(image_id, instance_type, security_group, script_path=None):

    # Provision and launch the EC2 instance
    ec2_client = boto3.client(
        'ec2',
        aws_access_key_id=utils.user.ACCESS_KEY,
        aws_secret_access_key=utils.user.SECRET_KEY)

    try:
        if script_path != None:
            with open(script_path, 'r') as f:
                script = '\n'.join(f)
                response = ec2_client.run_instances(ImageId=image_id,
                                                    InstanceType=instance_type,
                                                    KeyName=utils.user.KEY_PAIR,
                                                    MinCount=1,
                                                    MaxCount=1,
                                                    SecurityGroups=security_group,
                                                    UserData=script)
        else:
            response = ec2_client.run_instances(ImageId=image_id,
                                                    InstanceType=instance_type,
                                                    KeyName=utils.user.KEY_PAIR,
                                                    MinCount=1,
                                                    MaxCount=1,
                                                    SecurityGroups=security_group)
                                            

        instanceId = response['Instances'][0]["InstanceId"]

        try:
            ec2_client.get_waiter('instance_running').wait(InstanceIds=[instanceId])
            response_final = ec2_client.describe_instances(InstanceIds=[instanceId])
    
        except WaiterError as e:
            print(e)

    except ClientError as e:
        print(e)
        return None
    
    return response_final['Reservations'][0]['Instances'][0]


def create_security_group(name, permissions):    
    ec2_client = boto3.client(
        'ec2',
        aws_access_key_id=utils.user.ACCESS_KEY,
        aws_secret_access_key=utils.user.SECRET_KEY)

    response = ec2_client.describe_vpcs()
    vpc_id = response.get('Vpcs', [{}])[0].get('VpcId', '')

    try:
        response = ec2_client.create_security_group(GroupName=name,
                                            Description="DESCRIPTION",
                                            VpcId=vpc_id)
        security_group_id = response['GroupId']
        print('Security Group Created %s in vpc %s.' % (security_group_id, vpc_id))

        data = ec2_client.authorize_security_group_ingress(
            GroupId=security_group_id,
            IpPermissions=permissions)
        print('Ingress Successfully Set %s' % data)

    except ClientError as e:
        print(e)

    return security_group_id


def execute_cmds_ssh(instance_ip, user, cmds):
    
    key = paramiko.RSAKey.from_private_key_file(utils.user.KEY_PATH)
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

    # Connect/ssh to an instance
    try:
        client.connect(hostname=instance_ip, username=user, pkey=key)

        # Execute a command(cmd) after connecting/ssh to an instance
        for cmd in cmds:
            stdin, stdout, stderr = client.exec_command(cmd, get_pty=False)
            print(stdout.read().decode("utf-8"))

        return "Complete"
        
    except Exception as e:
        print(e)
        return "Failed"

    finally:
        # Close the client connection once the job is done
        client.close()
    

def execute_bg(instance_ip, user, cmd):
    
    key = paramiko.RSAKey.from_private_key_file(utils.user.KEY_PATH)
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

    # Connect/ssh to an instance
    try:
        client.connect(hostname=instance_ip, username=user, pkey=key)

        # Execute a command(cmd) after connecting/ssh to an instance
        transport = client.get_transport()
        channel = transport.open_session()
        channel.exec_command(cmd)
        return "Complete"
        
    except Exception as e:
        print(e)
        return "Failed"

    finally:
        # Close the client connection once the job is done
        client.close()


def scp_to_instance(instance_ip, user, file_path):

    key = paramiko.RSAKey.from_private_key_file(utils.user.KEY_PATH)
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

    # Connect/ssh to an instance
    try:
        client.connect(hostname=instance_ip, username=user, pkey=key)
        
        try:
            scp_client = client.open_sftp()
            scp_client.put(file_path, file_path)

        except Exception as e:
            print(e)

        finally:
            scp_client.close()

    except Exception as e:
        print(e)

    finally:
        # Close the client connection once the job is done
        client.close()


def exists(file_path, instance_ip, user):

    cmd = 'test -f %s && echo complete' % (file_path)
    
    key = paramiko.RSAKey.from_private_key_file(utils.user.KEY_PATH)
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

    # Connect/ssh to an instance
    try:
        client.connect(hostname=instance_ip, username=user, pkey=key)

        # Execute a command(cmd) after connecting/ssh to an instance
        while True:
            stdin, stdout, stderr = client.exec_command(cmd)
            res_str = stdout.read().decode("utf-8")
            print(res_str)
            if "complete" in res_str:
                break
            time.sleep(10)
        return True
        
    except Exception as e:
        print(e)
        return "Failed"

    finally:
        # Close the client connection once the job is done
        client.close()


def del_security_group(id):    
    ec2_client = boto3.client(
        'ec2',
        aws_access_key_id=utils.user.ACCESS_KEY,
        aws_secret_access_key=utils.user.SECRET_KEY)

    try:
        response = ec2_client.delete_security_group(GroupId=id)

    except ClientError as e:
        print(e)

    return response

def terminate_instances(ids):
    ec2_client = boto3.client(
        'ec2',
        aws_access_key_id=utils.user.ACCESS_KEY,
        aws_secret_access_key=utils.user.SECRET_KEY)

    try:
        ec2_client.terminate_instances(
                InstanceIds=ids)

        try:
            ec2_client.get_waiter('instance_terminated').wait(InstanceIds=ids)
            response_final = ec2_client.describe_instances(InstanceIds=ids)
    
        except WaiterError as e:
            print(e)

    except ClientError as e:
        print(e)

    print(response_final)
    return response_final
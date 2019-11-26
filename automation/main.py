# create virtualenv, install awscli and boto3

# Copyright 2010-2019 Amazon.com, Inc. or its affiliates. All Rights Reserved.
#
# This file is licensed under the Apache License, Version 2.0 (the "License").
# You may not use this file except in compliance with the License. A copy of the
# License is located at
#
# http://aws.amazon.com/apache2.0/
#
# This file is distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS
# OF ANY KIND, either express or implied. See the License for the specific
# language governing permissions and limitations under the License. 

from utils import create_ec2_instance, create_security_group
import logging


def main():
    # Assign these values before running the program
    # Use argparse + os.environ? AWS_ACCESS_KEY_ID / AWS_SECRET_ACCESS_KEY
    keypair_name = 'pencilleaf-key-pair'
    # ACCESS_KEY='AKIA54KY4G4NY2FMI4GT'
    # SECRET_KEY='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'
    AMI = 'ami-05c859630889c79c8'
    INSTANCE_TYPE = 't2.micro'


    # Set up logging
    logging.basicConfig(level=logging.DEBUG,
                        format='%(levelname)s: %(asctime)s: %(message)s')

    # # Create security group
    # flask_permissions = [{'IpProtocol': 'tcp',
    #                         'FromPort': 80,
    #                         'ToPort': 80,
    #                         'IpRanges': [{'CidrIp': '0.0.0.0/0'}]},
    #                         {'IpProtocol': 'tcp',
    #                         'FromPort': 22,
    #                         'ToPort': 22,
    #                         'IpRanges': [{'CidrIp': '0.0.0.0/0'}]},
    #                         {'IpProtocol': 'tcp',
    #                         'FromPort': 5000,
    #                         'ToPort': 5000,
    #                         'IpRanges': [{'CidrIp': '0.0.0.0/0'}]}]

    # flask_security_group = create_security_group("flask-webapp", flask_permissions)

    # # Provision and launch the EC2 instance
    # flask_instance_info = create_ec2_instance(AMI, INSTANCE_TYPE, keypair_name, ["flask-webapp"])

    # if flask_instance_info is not None:
    #     logging.info('Started ec2 instance for flask webapp')
    #     logging.info(f'Launched EC2 Instance {flask_instance_info["InstanceId"]}')
    #     logging.info(f'    VPC ID: {flask_instance_info["VpcId"]}')
    #     logging.info(f'    Private IP Address: {flask_instance_info["PrivateIpAddress"]}')
    #     logging.info(f'    Public IP Address: {flask_instance_info["PublicIpAddress"]}')
    #     logging.info(f'    Current State: {flask_instance_info["State"]["Name"]}')




    SQL_SCRIPT = "sql_script.sh"

    sql_permissions = [{'IpProtocol': 'tcp',
                            'FromPort': 22,
                            'ToPort': 22,
                            'IpRanges': [{'CidrIp': '0.0.0.0/0'}]}, # temporary, so that can ssh into it and check
                            {'IpProtocol': 'tcp',
                            'FromPort': 3306,
                            'ToPort': 3306,
                            'IpRanges': [{'CidrIp': '18.136.201.60' + '/32'}]}] # only allow flask to access mysql

    sql_security_group = create_security_group("mysql-server", sql_permissions)

    sql_instance_info = create_ec2_instance(AMI, INSTANCE_TYPE, keypair_name, ["mysql-server"], SQL_SCRIPT)

    if sql_instance_info is not None:
        logging.info('Started ec2 instance for mysql server')
        logging.info(f'Launched EC2 Instance {sql_instance_info["InstanceId"]}')
        logging.info(f'    VPC ID: {sql_instance_info["VpcId"]}')
        logging.info(f'    Private IP Address: {sql_instance_info["PrivateIpAddress"]}')
        logging.info(f'    Public IP Address: {sql_instance_info["PublicIpAddress"]}')
        logging.info(f'    Current State: {sql_instance_info["State"]["Name"]}')




    MONGO_SCRIPT = ""

    mongo_permissions = [{'IpProtocol': 'tcp',
                            'FromPort': 22,
                            'ToPort': 22,
                            'IpRanges': [{'CidrIp': '0.0.0.0/0'}]}, # temporary, so that can ssh into it and check
                            {'IpProtocol': 'tcp',
                            'FromPort': 27017,
                            'ToPort': 27017,
                            'IpRanges': [{'CidrIp': '18.136.201.60' + '/32'}]}] # only allow flask to access mongo
        
    mongo_security_group = create_security_group("mongo_db", mongo_permissions)

    mongo_instance_info = create_ec2_instance(AMI, INSTANCE_TYPE, keypair_name, ["mongo_db"], MONGO_SCRIPT)

    if mongo_instance_info is not None:
        logging.info('Started ec2 instance for mongo db')
        logging.info(f'Launched EC2 Instance {mongo_instance_info["InstanceId"]}')
        logging.info(f'    VPC ID: {mongo_instance_info["VpcId"]}')
        logging.info(f'    Private IP Address: {mongo_instance_info["PrivateIpAddress"]}')
        logging.info(f'    Public IP Address: {mongo_instance_info["PublicIpAddress"]}')
        logging.info(f'    Current State: {mongo_instance_info["State"]["Name"]}')


if __name__ == '__main__':
    main()
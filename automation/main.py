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

from utils import create_ec2_instance, create_security_group, check_if_complete, scp_to_instance, execute_cmd_ssh
import logging
import os
from time import sleep
import urllib.request



def main():

    LOCAL_IP = urllib.request.urlopen('https://ident.me').read().decode('utf8')

    KEY_PAIR = os.environ['KEY_PAIR']
   
   # How to get pem file??
    KEY_PATH = "C:\\Users\\x-cla\\Desktop\\Term 6\\50.043 Databases\\PROJECT\\pencilleaf-key-pair.pem"


    AMAZON_LINUX_AMI = 'ami-05c859630889c79c8'
    UBUNTU_AMI = 'ami-061eb2b23f9f8839c'
    INSTANCE_TYPE = 't2.micro'
    
    


    # Set up logging
    logging.basicConfig(level=logging.DEBUG,
                        format='%(levelname)s: %(asctime)s: %(message)s')

    # Create security group
    flask_permissions = [{'IpProtocol': 'tcp',
                            'FromPort': 22,
                            'ToPort': 22,
                            'IpRanges': [{'CidrIp': LOCAL_IP + '/32'}]},
                            {'IpProtocol': 'tcp',
                            'FromPort': 5000,
                            'ToPort': 5000,
                            'IpRanges': [{'CidrIp': '0.0.0.0/0'}]}]

    flask_security_group = create_security_group("flask-webapp", flask_permissions)

    # Provision and launch the EC2 instance
    flask_instance_info = create_ec2_instance(UBUNTU_AMI, INSTANCE_TYPE, KEY_PAIR, ["flask-webapp"])

    if flask_instance_info is not None:
        logging.info('Started ec2 instance for flask webapp')
        logging.info(f'Launched EC2 Instance {flask_instance_info["InstanceId"]}')
        logging.info(f'    VPC ID: {flask_instance_info["VpcId"]}')
        logging.info(f'    Private IP Address: {flask_instance_info["PrivateIpAddress"]}')
        logging.info(f'    Public IP Address: {flask_instance_info["PublicIpAddress"]}')
        logging.info(f'    Current State: {flask_instance_info["State"]["Name"]}')

    FLASK_IP = flask_instance_info["PublicIpAddress"]
    FLASK_ID = flask_instance_info["InstanceId"]



    SQL_SCRIPT = "sql_script.sh"

    sql_permissions = [{'IpProtocol': 'tcp',
                            'FromPort': 22,
                            'ToPort': 22,
                            'IpRanges': [{'CidrIp': LOCAL_IP + '/32'}]}, # temporary, so that can ssh into it and check
                            {'IpProtocol': 'tcp',
                            'FromPort': 3306,
                            'ToPort': 3306,
                            'IpRanges': [{'CidrIp': FLASK_IP + '/32'},
                                        {'CidrIp': LOCAL_IP + '/32'}]}] # only allow flask to access mysql

    sql_security_group = create_security_group("mysql-server", sql_permissions)

    sql_instance_info = create_ec2_instance(AMAZON_LINUX_AMI, INSTANCE_TYPE, KEY_PAIR, ["mysql-server"], SQL_SCRIPT)

    if sql_instance_info is not None:
        logging.info('Started ec2 instance for mysql server')
        logging.info(f'Launched EC2 Instance {sql_instance_info["InstanceId"]}')
        logging.info(f'    VPC ID: {sql_instance_info["VpcId"]}')
        logging.info(f'    Private IP Address: {sql_instance_info["PrivateIpAddress"]}')
        logging.info(f'    Public IP Address: {sql_instance_info["PublicIpAddress"]}')
        logging.info(f'    Current State: {sql_instance_info["State"]["Name"]}')

    MYSQL_IP = sql_instance_info["PublicIpAddress"]
    MYSQL_ID = sql_instance_info["InstanceId"]
    
    logging.info("Setting up mysql...")




    MONGO_SCRIPT = "mongo_script.sh"

    mongo_permissions = [{'IpProtocol': 'tcp',
                            'FromPort': 22,
                            'ToPort': 22,
                            'IpRanges': [{'CidrIp': LOCAL_IP + '/32'}]}, # temporary, so that can ssh into it and check
                            {'IpProtocol': 'tcp',
                            'FromPort': 27017,
                            'ToPort': 27017,
                            'IpRanges': [{'CidrIp': FLASK_IP + '/32'},
                                        {'CidrIp': LOCAL_IP + '/32'}]}]
        
    mongo_security_group = create_security_group("mongo_db", mongo_permissions)

    mongo_instance_info = create_ec2_instance(UBUNTU_AMI, INSTANCE_TYPE, KEY_PAIR, ["mongo_db"], MONGO_SCRIPT)

    if mongo_instance_info is not None:
        logging.info('Started ec2 instance for mongo db')
        logging.info(f'Launched EC2 Instance {mongo_instance_info["InstanceId"]}')
        logging.info(f'    VPC ID: {mongo_instance_info["VpcId"]}')
        logging.info(f'    Private IP Address: {mongo_instance_info["PrivateIpAddress"]}')
        logging.info(f'    Public IP Address: {mongo_instance_info["PublicIpAddress"]}')
        logging.info(f'    Current State: {mongo_instance_info["State"]["Name"]}')

    MONGO_IP = mongo_instance_info["PublicIpAddress"]
    MONGO_ID = mongo_instance_info["InstanceId"]


    logging.info("Databases are up")


    logging.info("Setting up mongodb...")
    
    boot_file_path = "/var/lib/cloud/instances/%s/boot-finished" % (MYSQL_ID)
    while True:
        if check_if_complete(boot_file_path, MYSQL_IP, "ec2-user", KEY_PATH):
            break
        sleep(10)

    logging.info("Databases are up")


    scp_to_instance(FLASK_IP, "ubuntu", KEY_PATH, "flask_script.sh")
    cmds = ["sed -i -e 's/\r$//' flask_script.sh", ". flask_script.sh %s %s" % (MYSQL_IP, MONGO_IP)]
    for cmd in cmds:
        execute_cmd_ssh(FLASK_IP, "ubuntu", KEY_PATH, cmd)

    indicator_file_path = "/home/ubuntu/script-finished"
    while True:
        if check_if_complete(indicator_file_path, FLASK_IP, "ubuntu", KEY_PATH):
            break
        sleep(10)

    logging.info("Flask server has started, please visit %s:5000/isit" % (FLASK_IP))


if __name__ == '__main__':
    main()
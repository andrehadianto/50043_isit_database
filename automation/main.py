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

from utils.utils import create_ec2_instance, create_security_group, execute_cmds_ssh, exists, execute_bg
import logging
import os
import urllib.request
import argparse

import utils.user as user



def main():
    
    LOCAL_IP = urllib.request.urlopen('http://ident.me').read().decode('utf8')

    AMAZON_LINUX_AMI = 'ami-05c859630889c79c8'
    UBUNTU_AMI = 'ami-061eb2b23f9f8839c'
    INSTANCE_TYPE = 't2.micro'

    # Set up logging
    logging.basicConfig(level=logging.INFO,
                        format='%(levelname)s: %(asctime)s: %(message)s')

    flask_script = os.path.join("scripts", "flask_script.sh")
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
    flask_instance_info = create_ec2_instance(UBUNTU_AMI, INSTANCE_TYPE, ["flask-webapp"], flask_script)

    if flask_instance_info is not None:
        logging.info('Started ec2 instance for flask webapp')
        logging.info(f'Launched EC2 Instance {flask_instance_info["InstanceId"]}')
        logging.info(f'    VPC ID: {flask_instance_info["VpcId"]}')
        logging.info(f'    Private IP Address: {flask_instance_info["PrivateIpAddress"]}')
        logging.info(f'    Public IP Address: {flask_instance_info["PublicIpAddress"]}')
        logging.info(f'    Current State: {flask_instance_info["State"]["Name"]}')

    FLASK_IP = flask_instance_info["PublicIpAddress"]
    FLASK_ID = flask_instance_info["InstanceId"]



    SQL_SCRIPT = os.path.join("scripts", "sql_script.sh")

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

    sql_instance_info = create_ec2_instance(AMAZON_LINUX_AMI, INSTANCE_TYPE, ["mysql-server"], SQL_SCRIPT)

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




    MONGO_SCRIPT = os.path.join("scripts", "mongo_script.sh")

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

    mongo_instance_info = create_ec2_instance(UBUNTU_AMI, INSTANCE_TYPE, ["mongo_db"], MONGO_SCRIPT)

    if mongo_instance_info is not None:
        logging.info('Started ec2 instance for mongo db')
        logging.info(f'Launched EC2 Instance {mongo_instance_info["InstanceId"]}')
        logging.info(f'    VPC ID: {mongo_instance_info["VpcId"]}')
        logging.info(f'    Private IP Address: {mongo_instance_info["PrivateIpAddress"]}')
        logging.info(f'    Public IP Address: {mongo_instance_info["PublicIpAddress"]}')
        logging.info(f'    Current State: {mongo_instance_info["State"]["Name"]}')

    MONGO_IP = mongo_instance_info["PublicIpAddress"]
    MONGO_ID = mongo_instance_info["InstanceId"]

    
    logging.info("Setting up the flask webapp...")

    # Check if script is finished
    indicator_file_path = "/var/lib/cloud/instances/%s/boot-finished" % (FLASK_ID)
    while True:
        test = exists(indicator_file_path, FLASK_IP, "ubuntu")
        if test == "Failed":
            print("Connection failed, retrying...")
            continue
        else:
            break

    cmds = [
        "sudo touch /50043_isit_database-master/server/.env && echo Created .env file",
        """sudo tee -a /50043_isit_database-master/server/.env > /dev/null << EOT
            SQL_DB=isit_database
            SQL_USER=root
            SQL_PW=password
            SQL_HOST=%s
            MONGO_DB=isit_database_mongo
            LOG_DB=log_mongo
            MONGO_HOST=%s""" % (MYSQL_IP, MONGO_IP)
    ]

    while True:
        test = execute_cmds_ssh(FLASK_IP, "ubuntu", cmds)
        if test == "Failed":
            print("Connection failed, retrying...")
            continue
        else:
            break
    
    while True:
        test = execute_bg(FLASK_IP, "ubuntu", "sudo nohup python3 /50043_isit_database-master/server/app.py < /dev/null > /50043_isit_database-master/server/log.txt 2>&1 &")
        if test == "Failed":
            print("Connection failed, retrying...")
            continue
        else:
            break   
    
    logging.info("Mongodb can be found at %s" % (MONGO_IP))
    logging.info("MySQL database can be found at %s" % (MYSQL_IP))
    logging.info("Flask server has started, please visit %s:5000/isit" % (FLASK_IP))

if __name__ == '__main__':

    parser = argparse.ArgumentParser()
    parser.add_argument("access", help="AWS access key")
    parser.add_argument("secret", help="Your secret access key")
    parser.add_argument("keypair", help="AWS key pair")
    parser.add_argument("keypath", help="Absolute path of your .pem file")
    args = parser.parse_args()

    # Set up variables
    user.init()
    
    user.ACCESS_KEY = args.access
    user.SECRET_KEY = args.secret
    user.KEY_PAIR = args.keypair
    user.KEY_PATH = args.keypath

    main()
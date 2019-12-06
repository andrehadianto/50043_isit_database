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
import yaml

import utils.user as user


def main():
    
    LOCAL_IP = urllib.request.urlopen('http://ident.me').read().decode('utf8')

    AMAZON_LINUX_AMI = 'ami-05c859630889c79c8'
    UBUNTU_AMI = 'ami-061eb2b23f9f8839c'
    INSTANCE_TYPE = 't2.micro'

    HADOOP_SCRIPT = os.path.join("scripts", "hadoop_script.sh")
    FLASK_SCRIPT = os.path.join("scripts", "flask_script.sh")
    SQL_SCRIPT = os.path.join("scripts", "sql_script.sh")
    MONGO_SCRIPT = os.path.join("scripts", "mongo_script.sh")

    CONFIG = dict()
    CONFIG["AWS_CREDENTIALS"] = {"ACCESS_KEY": user.ACCESS_KEY,"SECRET_KEY": user.SECRET_KEY, "KEY_PAIR": user.KEY_PAIR, "KEY_PATH": user.KEY_PATH}

    # Set up logging
    logging.basicConfig(level=logging.INFO,
                        format='%(levelname)s: %(asctime)s: %(message)s')

    # # Create security group
    # flask_permissions = [{'IpProtocol': 'tcp',
    #                         'FromPort': 22,
    #                         'ToPort': 22,
    #                         'IpRanges': [{'CidrIp': LOCAL_IP + '/32'}]},
    #                         {'IpProtocol': 'tcp',
    #                         'FromPort': 5000,
    #                         'ToPort': 5000,
    #                         'IpRanges': [{'CidrIp': '0.0.0.0/0'}]}]

    # flask_security_group = create_security_group("flask-webapp", flask_permissions)
    # CONFIG["SECURITY_GROUPS"] = [flask_security_group]

    # # Provision and launch the EC2 instance
    # flask_instance_info = create_ec2_instance(1, UBUNTU_AMI, INSTANCE_TYPE, ["flask-webapp"], FLASK_SCRIPT)[0]

    # if flask_instance_info is not None:
    #     logging.info('Started ec2 instance for flask webapp')
    #     logging.info(f'Launched EC2 Instance {flask_instance_info["InstanceId"]}')
    #     logging.info(f'    VPC ID: {flask_instance_info["VpcId"]}')
    #     logging.info(f'    Private IP Address: {flask_instance_info["PrivateIpAddress"]}')
    #     logging.info(f'    Public IP Address: {flask_instance_info["PublicIpAddress"]}')
    #     logging.info(f'    Current State: {flask_instance_info["State"]["Name"]}')

    # CONFIG["FLASK"] = {"IP": flask_instance_info["PublicIpAddress"], "ID": flask_instance_info["InstanceId"]}





    hadoop_permissions = [{'IpProtocol': 'tcp',
                            'FromPort': 0,
                            'ToPort': 65535,
                            'IpRanges': [{'CidrIp': '0.0.0.0/0'}]}]

    hadoop_security_group = create_security_group("hadoop", hadoop_permissions)
    # CONFIG["SECURITY_GROUPS"].append(hadoop_security_group)
    CONFIG["SECURITY_GROUPS"] = [hadoop_security_group]
    logging.info('Starting hadoop namenodes and datanodes...')

    hadoop_instance_info = create_ec2_instance(int(user.NODES), UBUNTU_AMI, INSTANCE_TYPE, ["hadoop"], HADOOP_SCRIPT)

    if hadoop_instance_info is not None:
        for node in range(int(user.NODES)):
            logging.info(f'Launched hadoop instance {hadoop_instance_info[node]["InstanceId"]}')
            logging.info(f'    VPC ID: {hadoop_instance_info[node]["VpcId"]}')
            logging.info(f'    Private IP Address: {hadoop_instance_info[node]["PrivateIpAddress"]}')
            logging.info(f'    Public IP Address: {hadoop_instance_info[node]["PublicIpAddress"]}')
            logging.info(f'    Current State: {hadoop_instance_info[node]["State"]["Name"]}')

    CONFIG["MASTER"] = {"IP": hadoop_instance_info[0]["PublicIpAddress"], 
                                "ID": hadoop_instance_info[0]["InstanceId"],
                                "DNS": hadoop_instance_info[0]["PublicDnsName"]}
    CONFIG["SLAVES"] = [{"IP": hadoop_instance_info[i]["PublicIpAddress"], 
                                "ID": hadoop_instance_info[i]["InstanceId"],
                                "DNS": hadoop_instance_info[i]["PublicDnsName"]} for i in range(1, int(user.NODES))]



    # sql_permissions = [{'IpProtocol': 'tcp',
    #                         'FromPort': 22,
    #                         'ToPort': 22,
    #                         'IpRanges': [{'CidrIp': LOCAL_IP + '/32'}]}, # temporary, so that can ssh into it and check
    #                         {'IpProtocol': 'tcp',
    #                         'FromPort': 3306,
    #                         'ToPort': 3306,
    #                         'IpRanges': [{'CidrIp': CONFIG["FLASK"]["IP"] + '/32'},
    #                                     {'CidrIp': LOCAL_IP + '/32'},
    #                                     {'CidrIp': CONFIG["HADOOP_MASTER"]["IP"] + '/32'}]}] # only allow flask to access mysql

    # sql_security_group = create_security_group("mysql-server", sql_permissions)

    # CONFIG["SECURITY_GROUPS"].append(sql_security_group)

    # logging.info('Starting MySQL...')

    # sql_instance_info = create_ec2_instance(1,AMAZON_LINUX_AMI, INSTANCE_TYPE, ["mysql-server"], SQL_SCRIPT)[0]

    # if sql_instance_info is not None:
    #     logging.info('Started ec2 instance for mysql server')
    #     logging.info(f'Launched EC2 Instance {sql_instance_info["InstanceId"]}')
    #     logging.info(f'    VPC ID: {sql_instance_info["VpcId"]}')
    #     logging.info(f'    Private IP Address: {sql_instance_info["PrivateIpAddress"]}')
    #     logging.info(f'    Public IP Address: {sql_instance_info["PublicIpAddress"]}')
    #     logging.info(f'    Current State: {sql_instance_info["State"]["Name"]}')

    # CONFIG["MYSQL"] = {"IP": sql_instance_info["PublicIpAddress"], "ID": sql_instance_info["InstanceId"]}
    




   
    # mongo_permissions = [{'IpProtocol': 'tcp',
    #                         'FromPort': 22,
    #                         'ToPort': 22,
    #                         'IpRanges': [{'CidrIp': LOCAL_IP + '/32'}]}, # temporary, so that can ssh into it and check
    #                         {'IpProtocol': 'tcp',
    #                         'FromPort': 27017,
    #                         'ToPort': 27017,
    #                         'IpRanges': [{'CidrIp': CONFIG["FLASK"]["IP"] + '/32'},
    #                                     {'CidrIp': LOCAL_IP + '/32'},
    #                                     {'CidrIp': CONFIG["HADOOP_MASTER"] + '/32'}]}]
        
    # mongo_security_group = create_security_group("mongo_db", mongo_permissions)

    # CONFIG["SECURITY_GROUPS"].append(mongo_security_group)

    # logging.info('Starting MongoDB...')

    # mongo_instance_info = create_ec2_instance(1, UBUNTU_AMI, INSTANCE_TYPE, ["mongo_db"], MONGO_SCRIPT)[0]

    # if mongo_instance_info is not None:
    #     logging.info('Started ec2 instance for mongo db')
    #     logging.info(f'Launched EC2 Instance {mongo_instance_info["InstanceId"]}')
    #     logging.info(f'    VPC ID: {mongo_instance_info["VpcId"]}')
    #     logging.info(f'    Private IP Address: {mongo_instance_info["PrivateIpAddress"]}')
    #     logging.info(f'    Public IP Address: {mongo_instance_info["PublicIpAddress"]}')
    #     logging.info(f'    Current State: {mongo_instance_info["State"]["Name"]}')

    # CONFIG["MONGO"] = {"IP": mongo_instance_info["PublicIpAddress"], "ID": mongo_instance_info["InstanceId"]}




    with open('config/config.yml', 'w') as file:
        documents = yaml.dump(CONFIG, file)




    # logging.info("Setting up the flask webapp...")

    # # Check if script is finished
    # indicator_file_path = "/var/lib/cloud/instances/%s/boot-finished" % (CONFIG["FLASK"]["ID"])
    # while True:
    #     test = exists(indicator_file_path, CONFIG["FLASK"]["IP"], "ubuntu")
    #     if test == "Failed":
    #         print("Connection failed, retrying...")
    #         continue
    #     else:
    #         break

    # cmds = [
    #     "sudo touch /50043_isit_database-master/server/.env && echo Created .env file",
    #     """sudo tee -a /50043_isit_database-master/server/.env > /dev/null << EOT
    #         SQL_DB=isit_database
    #         SQL_USER=root
    #         SQL_PW=password
    #         SQL_HOST=%s
    #         MONGO_DB=isit_database_mongo
    #         LOG_DB=log_mongo
    #         MONGO_HOST=%s""" % (CONFIG["MYSQL"]["IP"], CONFIG["MONGO"]["IP"])
    # ]

    # while True:
    #     test = execute_cmds_ssh(CONFIG["FLASK"]["IP"], "ubuntu", cmds)
    #     if test == "Failed":
    #         print("Connection failed, retrying...")
    #         continue
    #     else:
    #         break
    
    # while True:
    #     test = execute_bg(CONFIG["FLASK"]["IP"], "ubuntu", "sudo nohup python3 /50043_isit_database-master/server/app.py < /dev/null > /50043_isit_database-master/server/log.txt 2>&1 &")
    #     if test == "Failed":
    #         print("Connection failed, retrying...")
    #         continue
    #     else:
    #         break   

    # logging.info("MongoDB can be found at %s" % (CONFIG["MONGO"]["IP"]))
    # logging.info("MySQL database can be found at %s" % (CONFIG["MYSQL"]["IP"]))
    # logging.info("Flask server has started, please visit %s:5000/isit" % (CONFIG["FLASK"]["IP"]))
 


if __name__ == '__main__':

    parser = argparse.ArgumentParser()
    parser.add_argument("access", help="AWS access key")
    parser.add_argument("secret", help="Your secret access key")
    parser.add_argument("keypair", help="AWS key pair")
    parser.add_argument("keypath", help="Absolute path of your .pem file")
    parser.add_argument("nodes", help="Number of datanodes to spin up", type=int, choices=[1,2,4,8])
    args = parser.parse_args()

    # Set up variables
    user.init()
    user.ACCESS_KEY = args.access
    user.SECRET_KEY = args.secret
    user.KEY_PAIR = args.keypair
    user.KEY_PATH = args.keypath
    user.NODES = args.nodes

    main()
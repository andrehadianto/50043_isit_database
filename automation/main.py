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

from utils.utils import create_ec2_instance, create_security_group, execute_cmds_ssh, exists, execute_bg, run_command_bash
import logging
import os
import urllib.request
import argparse
import yaml
import subprocess
import time

import utils.user as user


def main():

    # Set up variables
    LOCAL_IP = urllib.request.urlopen('http://ident.me').read().decode('utf8')

    AMAZON_LINUX_AMI = 'ami-05c859630889c79c8'
    UBUNTU_AMI = 'ami-061eb2b23f9f8839c'
    INSTANCE_TYPE = 't2.micro'
    HADOOP_INSTANCE_TYPE='t2.medium'

    HADOOP_SCRIPT = os.path.join("scripts", "hadoop_script.sh")
    FLASK_SCRIPT = os.path.join("scripts", "flask_script.sh")
    SQL_SCRIPT = os.path.join("scripts", "sql_script.sh")
    MONGO_SCRIPT = os.path.join("scripts", "mongo_script.sh")

    HADOOP_CONFIG_SCRIPT = os.path.join("scripts", "{}nodesetup".format(user.NODES), "initialize_hadoop_setup.sh")

    CONFIG = dict()
    CONFIG["AWS_CREDENTIALS"] = {"ACCESS_KEY": user.ACCESS_KEY,"SECRET_KEY": user.SECRET_KEY, "KEY_PAIR": user.KEY_PAIR, "KEY_PATH": user.KEY_PATH}


    # Set up logging
    logging.basicConfig(level=logging.INFO,
                        format='%(levelname)s: %(asctime)s: %(message)s')


    # *=================================================*
    # *                     FLASK                       *
    # *=================================================*

    # Create security group for flask
    flask_permissions = [{'IpProtocol': 'tcp',
                            'FromPort': 22,
                            'ToPort': 22,
                            'IpRanges': [{'CidrIp': LOCAL_IP + '/32'}]},
                            {'IpProtocol': 'tcp',
                            'FromPort': 5000,
                            'ToPort': 5000,
                            'IpRanges': [{'CidrIp': '0.0.0.0/0'}]}]

    flask_security_group = create_security_group("flask-webapp", flask_permissions)
    CONFIG["SECURITY_GROUPS"] = [flask_security_group]

    # Provision and launch the EC2 instance for flask
    logging.info('Starting flask instance...')

    flask_instance_info = create_ec2_instance(1, UBUNTU_AMI, INSTANCE_TYPE, ["flask-webapp"], FLASK_SCRIPT)[0]

    if flask_instance_info is not None:
        logging.info('Started ec2 instance for flask webapp')
        logging.info(f'Launched EC2 Instance {flask_instance_info["InstanceId"]}')
        logging.info(f'    VPC ID: {flask_instance_info["VpcId"]}')
        logging.info(f'    Private IP Address: {flask_instance_info["PrivateIpAddress"]}')
        logging.info(f'    Public IP Address: {flask_instance_info["PublicIpAddress"]}')
        logging.info(f'    Current State: {flask_instance_info["State"]["Name"]}')

    CONFIG["FLASK"] = {"IP": flask_instance_info["PublicIpAddress"], "ID": flask_instance_info["InstanceId"],"DNS": flask_instance_info["PublicDnsName"]}


    # *=================================================*
    # *                     HADOOP                      *
    # *=================================================*

    # Create security group for hadoop/spark instances
    hadoop_permissions = [{'IpProtocol': 'tcp',
                            'FromPort': 0,
                            'ToPort': 65535,
                            'IpRanges': [{'CidrIp': '0.0.0.0/0'}]}]

    hadoop_security_group = create_security_group("hadoop", hadoop_permissions)

    CONFIG["SECURITY_GROUPS"].append(hadoop_security_group)

    # Provision and launch the EC2 instances for hadoop/spark
    logging.info('Starting hadoop namenodes and datanodes...')

    hadoop_instance_info = create_ec2_instance(int(user.NODES), UBUNTU_AMI, HADOOP_INSTANCE_TYPE, ["hadoop"], HADOOP_SCRIPT)

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
    
    # *=================================================*
    # *                     MYSQL                       *
    # *=================================================*

    # Create security group for mysql
    sql_permissions = [{'IpProtocol': 'tcp',
                            'FromPort': 22,
                            'ToPort': 22,
                            'IpRanges': [{'CidrIp': LOCAL_IP + '/32'}]}, # temporary, so that can ssh into it and check
                            {'IpProtocol': 'tcp',
                            'FromPort': 3306,
                            'ToPort': 3306,
                            'IpRanges': [{'CidrIp': CONFIG["FLASK"]["IP"] + '/32'},
                                        {'CidrIp': LOCAL_IP + '/32'},
                                        {'CidrIp': CONFIG["MASTER"]["IP"] + '/32'}]}]

    sql_security_group = create_security_group("mysql-server", sql_permissions)

    CONFIG["SECURITY_GROUPS"].append(sql_security_group)

    # Provision and launch the EC2 instance for mysql
    logging.info('Starting MySQL...')

    sql_instance_info = create_ec2_instance(1,AMAZON_LINUX_AMI, INSTANCE_TYPE, ["mysql-server"], SQL_SCRIPT)[0]

    if sql_instance_info is not None:
        logging.info('Started ec2 instance for mysql server')
        logging.info(f'Launched EC2 Instance {sql_instance_info["InstanceId"]}')
        logging.info(f'    VPC ID: {sql_instance_info["VpcId"]}')
        logging.info(f'    Private IP Address: {sql_instance_info["PrivateIpAddress"]}')
        logging.info(f'    Public IP Address: {sql_instance_info["PublicIpAddress"]}')
        logging.info(f'    Current State: {sql_instance_info["State"]["Name"]}')

    CONFIG["MYSQL"] = {"IP": sql_instance_info["PublicIpAddress"], "ID": sql_instance_info["InstanceId"]}
    

    # *=================================================*
    # *                     MONGO                       *
    # *=================================================*
    
   # Create security group for mongo
    mongo_permissions = [{'IpProtocol': 'tcp',
                            'FromPort': 22,
                            'ToPort': 22,
                            'IpRanges': [{'CidrIp': LOCAL_IP + '/32'}]}, # temporary, so that can ssh into it and check
                            {'IpProtocol': 'tcp',
                            'FromPort': 27017,
                            'ToPort': 27017,
                            'IpRanges': [{'CidrIp': CONFIG["FLASK"]["IP"] + '/32'},
                                        {'CidrIp': LOCAL_IP + '/32'},
                                        {'CidrIp': CONFIG["MASTER"]["IP"] + '/32'}]}]
        
    mongo_security_group = create_security_group("mongo_db", mongo_permissions)

    CONFIG["SECURITY_GROUPS"].append(mongo_security_group)

    # Provision and launch EC2 instance for mongo
    logging.info('Starting MongoDB...')

    mongo_instance_info = create_ec2_instance(1, UBUNTU_AMI, INSTANCE_TYPE, ["mongo_db"], MONGO_SCRIPT)[0]

    if mongo_instance_info is not None:
        logging.info('Started ec2 instance for mongo db')
        logging.info(f'Launched EC2 Instance {mongo_instance_info["InstanceId"]}')
        logging.info(f'    VPC ID: {mongo_instance_info["VpcId"]}')
        logging.info(f'    Private IP Address: {mongo_instance_info["PrivateIpAddress"]}')
        logging.info(f'    Public IP Address: {mongo_instance_info["PublicIpAddress"]}')
        logging.info(f'    Current State: {mongo_instance_info["State"]["Name"]}')

    CONFIG["MONGO"] = {"IP": mongo_instance_info["PublicIpAddress"], "ID": mongo_instance_info["InstanceId"]}




    # Dump info to config.yml
    with open('config/config.yml', 'w') as file:
        documents = yaml.dump(CONFIG, file)




    # *=================================================*
    # *                 FLASK CONFIG                    *
    # *=================================================*

    logging.info("Setting up the flask webapp...")

    # Check if script is finished
    indicator_file_path = "/var/lib/cloud/instances/%s/boot-finished" % (CONFIG["FLASK"]["ID"])
    while True:
        test = exists(indicator_file_path, CONFIG["FLASK"]["IP"], "ubuntu")
        if test == "Failed":
            print("Connection failed, retrying...")
            continue
        else:
            break

    # Create .env file for flask to connect to mongo/mysql
    cmds = [
        "sudo touch /50043_isit_database-master/server/.env && echo Created .env file",
        """sudo tee -a /50043_isit_database-master/server/.env > /dev/null << EOT
            SQL_DB=isit_database
            SQL_USER=root
            SQL_PW=password
            SQL_HOST=%s
            MONGO_DB=isit_database_mongo
            LOG_DB=log_mongo
            MONGO_HOST=%s""" % (CONFIG["MYSQL"]["IP"], CONFIG["MONGO"]["IP"])]
    
    while True:
        test = execute_cmds_ssh(CONFIG["FLASK"]["IP"], "ubuntu", cmds)
        if test == "Failed":
            print("Connection failed, retrying...")
            continue
        else:
            break
    
    # Run flask app in background (no hang up)
    while True:
        test = execute_bg(CONFIG["FLASK"]["IP"], "ubuntu", "sudo nohup python3 /50043_isit_database-master/server/app.py < /dev/null > /50043_isit_database-master/server/log.txt 2>&1 &")
        if test == "Failed":
            print("Connection failed, retrying...")
            continue
        else:
            break   

    logging.info("MongoDB can be found at %s" % (CONFIG["MONGO"]["IP"]))
    logging.info("MySQL database can be found at %s" % (CONFIG["MYSQL"]["IP"]))
    logging.info("Flask server has started, please visit %s:5000/isit" % (CONFIG["FLASK"]["IP"]))
    

    # *=================================================*
    # *                 HADOOP CONFIG                   *
    # *=================================================*

    # Check if hadoop/spark installed
    indicator_file_path = "/var/lib/cloud/instances/%s/boot-finished" % (CONFIG["MASTER"]["ID"])
    while True:
        test = exists(indicator_file_path, CONFIG["MASTER"]["IP"], "ubuntu")
        if test == "Failed":
            print("Connection failed, retrying...")
            continue
        else:
            break

    # Call bash script to do config for hadoop/spark (set up passwordless ssh, start hdfs and spark processes)

    # 2node: keypath, master dns, slave dns, slave ip
    # 4node: keypath, master dns, slave1 dns, slave2 dns, slave3 dns, slave4 dns, slave1 ip, slave2 ip, slave3 ip, slave4 ip

    prefix = ["/bin/bash", HADOOP_CONFIG_SCRIPT, CONFIG["AWS_CREDENTIALS"]["KEY_PATH"], CONFIG["MASTER"]["DNS"]]
    slave_dns = [i["DNS"] for i in CONFIG["SLAVES"]]
    slave_ip = [i["IP"] for i in CONFIG["SLAVES"]]
    process_cmd = prefix + slave_dns + slave_ip

    print(process_cmd)
    time.sleep(60)
    run_command_bash(process_cmd)

    time.sleep(5)
    ANALYTICS_SCRIPT = "scripts/analytics/analytics.sh"
    analytics = ['/bin/bash', ANALYTICS_SCRIPT, CONFIG["AWS_CREDENTIALS"]["KEY_PATH"], CONFIG["MASTER"]["IP"], CONFIG["MONGO"]["IP"], CONFIG["MYSQL"]["IP"]]
    run_command_bash(analytics)

    logging.info("MongoDB can be found at %s" % (CONFIG["MONGO"]["IP"]))
    logging.info("MySQL database can be found at %s" % (CONFIG["MYSQL"]["IP"]))
    logging.info("Flask server: %s:5000/isit" % (CONFIG["FLASK"]["IP"]))
    logging.info("Output files are stored in hdfs. Name node: %s" % (CONFIG["MASTER"]["DNS"]))
    logging.info("The output of the correlation coefficient can be found in /corr/ in the last file. E.g. part-000XX")
    logging.info("For more information, visit https://github.com/andrehadianto/50043_isit_database/tree/develop/#1-correlation")
    logging.info("Output of Task 2 can be found at /tfidf directory in hdfs")
    logging.info("For more information, visit https://github.com/andrehadianto/50043_isit_database/tree/develop/#2-tf-idf")

if __name__ == '__main__':

    parser = argparse.ArgumentParser()
    parser.add_argument("access", help="AWS access key")
    parser.add_argument("secret", help="Your secret access key")
    parser.add_argument("keypair", help="AWS key pair")
    parser.add_argument("keypath", help="Absolute path of your .pem file")
    parser.add_argument("nodes", help="Number of datanodes to spin up", type=int, choices=[2,4,8])
    args = parser.parse_args()

    # Set up variables
    user.init()
    user.ACCESS_KEY = args.access
    user.SECRET_KEY = args.secret
    user.KEY_PAIR = args.keypair
    user.KEY_PATH = args.keypath
    user.NODES = args.nodes

    main()
    

    
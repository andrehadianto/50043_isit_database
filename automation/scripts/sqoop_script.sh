#!/bin/bash

echo "=== Set Up for Sql-HDFS === "

echo "Installing Apache Sqoop..."
wget http://archive.apache.org/dist/sqoop/1.99.7/sqoop-1.99.7-bin-hadoop200.tar.gz
tar -xvf sqoop-1.99.7-bin-hadoop200.tar.gz
sudo mv sqoop-1.99.7-bin-hadoop200 /usr/lib/

# Set Hadoop-related environment variables
# export HADOOP_HOME=$HOME/hadoop-2.7.3
# export HADOOP_CONF_DIR=$HOME/hadoop-2.7.3/etc/hadoop
# export HADOOP_MAPRED_HOME=$HOME/hadoop-2.7.3
# export HADOOP_COMMON_HOME=$HOME/hadoop-2.7.3
# export HADOOP_HDFS_HOME=$HOME/hadoop-2.7.3
# export HADOOP_YARN_HOME=$HOME/hadoop-2.7.3

echo "Setting Sqoop ENV variables and PATH..."

sudo bash -c 'echo "export SQOOP_HOME=/usr/lib/sqoop-1.99.7-bin-hadoop200" >> /etc/profile'
sudo bash -c 'echo "export PATH=$PATH:$SQOOP_HOME/bin" >> /etc/profile'
sudo bash -c 'echo "export SQOOP_CONF_DIR=$SQOOP_HOME/conf" >> /etc/profile'
sudo bash -c 'echo "export SQOOP_CLASS_PATH=$SQOOP_CONF_DIR" >> /etc/profile'

source /etc/profile

echo "Copying Hadoop jar files..."
# copy Hadoop jar files to Sqoop server/lib/
cp -a /home/ubuntu/server/hadoop-2.8.5/share/hadoop/common/. /usr/lib/sqoop-1.99.7-bin-hadoop200/server/lib/
cp -a /home/ubuntu/server/hadoop-2.8.5/share/hadoop/common/lib/. /usr/lib/sqoop-1.99.7-bin-hadoop200/server/lib/
cp -a /home/ubuntu/server/hadoop-2.8.5/share/hadoop/hdfs/. /usr/lib/sqoop-1.99.7-bin-hadoop200/server/lib/
cp -a /home/ubuntu/server/hadoop-2.8.5/share/hadoop/hdfs/lib/. /usr/lib/sqoop-1.99.7-bin-hadoop200/server/lib/
cp -a /home/ubuntu/server/hadoop-2.8.5/share/hadoop/mapreduce/. /usr/lib/sqoop-1.99.7-bin-hadoop200/server/lib/
cp -a /home/ubuntu/server/hadoop-2.8.5/share/hadoop/mapreduce/lib/. /usr/lib/sqoop-1.99.7-bin-hadoop200/server/lib/
cp -a /home/ubuntu/server/hadoop-2.8.5/share/hadoop/yarn/. /usr/lib/sqoop-1.99.7-bin-hadoop200/server/lib/
cp -a /home/ubuntu/server/hadoop-2.8.5/share/hadoop/yarn/lib/. /usr/lib/sqoop-1.99.7-bin-hadoop200/server/lib/
echo "Copied Hadoop jar files..."

echo "Editing Hadoop core-site..."
# impersonate user access to HDFS
cat >> /home/ubuntu/server/hadoop-2.8.5/etc/hadoop/core-site.xml << EOF 
<property>
    <name>hadoop.proxyuser.ubuntu.hosts</name>
    <value>*</value>
</property>
<property>
    <name>hadoop.proxyuser.ubuntu.groups</name>
    <value>*</value>
</property>
EOF

echo "Initializing and starting Sqoop server..."
. /usr/lib/sqoop-1.99.7-bin-hadoop200/bin/sqoop2-tool upgrade
. /usr/lib/sqoop-1.99.7-bin-hadoop200/bin/sqoop2-server start

# ./sqoop.sh server tools [need args]
# ./sqoop.sh server start
# Setting conf dir: ./../conf
# Sqoop home directory: /usr/lib/sqoop-1.99.7-bin-hadoop200
# 'Cant load the Hadoop related java lib, please check the setting for the following environment variables:
#     HADOOP_COMMON_HOME, HADOOP_HDFS_HOME, HADOOP_MAPRED_HOME, HADOOP_YARN_HOME
# ubuntu@ip-172-31-29-2:/usr/lib/sqoop-1.99.7-bin-hadoop200/bin$'

echo "=== Sqoop setup done ==="

echo "Installing JDBC driver..."
wget http://dev.mysql.com/get/Downloads/Connector-J/mysql-connector-java-5.1.38.tar.gz
tar -xvzf mysql-connector-java-5.1.38.tar.gz
sudo cp mysql-connector-java-5.1.38/mysql-connector-java-5.1.38-bin.jar /usr/lib/sqoop-1.99.7-bin-hadoop200/server/lib/

echo "Importing Mysql data to HDFS..."
# EDIT
sqoop list-tables --connect jdbc:mysql://db-instance-endpoint/yourdatabase \
--username your-username --password your-pw \
--table your-table --columns "col1, col2" \
--target-dir /your-target-dir
# imports data as csv file

echo "=== Done importing kindle reviews to HDFS ==="
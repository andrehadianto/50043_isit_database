#!/bin/bash

echo "=== Set Up for Sql-HDFS === "

echo "Installing Apache Sqoop 1.4.7 Hadoop..."
wget https://www-us.apache.org/dist/sqoop/1.4.7/sqoop-1.4.7.bin__hadoop-2.6.0.tar.gz
tar -zxvf sqoop-1.4.7.bin__hadoop-2.6.0.tar.gz
sudo mv sqoop-1.4.7.bin__hadoop-2.6.0 /usr/lib

sudo chmod a+rw /etc/profile

echo "Setting ENV variables and path..."
cat >> /etc/profile << EOF 
export HADOOP_HOME=$HOME/server/hadoop-2.8.5
export SQOOP_HOME=/usr/lib/sqoop-1.4.7.bin__hadoop-2.6.0
EOF
source /etc/profile

cat >> /etc/profile << EOF 
export HADOOP_HOME=$HOME/server/hadoop-2.8.5
export HADOOP_CONF_DIR=$HADOOP_HOME/hadoop-2.8.5/etc/hadoop
export HADOOP_MAPRED_HOME=$HADOOP_HOME/share/hadoop/mapreduce
export HADOOP_COMMON_HOME=$HADOOP_HOME/share/hadoop/common
export HADOOP_HDFS_HOME=$HADOOP_HOME/share/hadoop/hdfs
export HADOOP_YARN_HOME=$HADOOP_HOME/share/hadoop/yarn
export PATH=$PATH:$SQOOP_HOME/bin
export SQOOP_CONF_DIR=$SQOOP_HOME/conf
EOF

source /etc/profile

# echo "Editing Hadoop core-site..."
# # impersonate user access to HDFS
# cat >> /home/ubuntu/server/hadoop-2.8.5/etc/hadoop/core-site.xml << EOF 
# <property>
#     <name>hadoop.proxyuser.ubuntu.hosts</name>
#     <value>*</value>
# </property>
# <property>
#     <name>hadoop.proxyuser.ubuntu.groups</name>
#     <value>*</value>
# </property>
# EOF

# # edit configurations for sqoop.properties file
# # http://brianoneill.blogspot.com/2014/10/sqoop-1993-w-hadoop-2-installation.html
# mkdir /home/ubuntu/server/hadoop-2.8.5/etc/hadoop/conf
# sed -i 's/org.apache.sqoop.submission.engine.mapreduce.configuration.directory=\/etc\/hadoop\/conf\//org.apache.sqoop.submission.engine.mapreduce.configuration.directory=\/home\/ubuntu\/server\/hadoop-2.8.5\/etc\/hadoop' \
# /usr/lib/sqoop-1.99.7-bin-hadoop200/conf/sqoop.properties

# echo "Initializing and starting Sqoop server..."
# /usr/lib/sqoop-1.99.7-bin-hadoop200/bin/sqoop2-tool upgrade
# /usr/lib/sqoop-1.99.7-bin-hadoop200/bin/sqoop2-server start

echo "Installing JDBC driver..."
wget http://dev.mysql.com/get/Downloads/Connector-J/mysql-connector-java-5.1.38.tar.gz
tar -xvzf mysql-connector-java-5.1.38.tar.gz
sudo cp mysql-connector-java-5.1.38/mysql-connector-java-5.1.38-bin.jar /usr/lib/sqoop-1.4.7.bin__hadoop-2.6.0/lib/

echo "=== Sqoop setup done ==="

echo "Importing Mysql data to HDFS..."
sqoop import --connect jdbc:mysql://3.0.78.199:3306/isit_database \
--username root --password password \
--table kindle_reviews \
--where "id < 5" \
--target-dir /home/ubuntu/kindle_reviews \
--as-textfile 

echo "=== Done importing kindle reviews to HDFS ==="


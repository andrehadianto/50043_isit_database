#!/bin/bash

sudo apt-get -y update
sleep 1 
# The prompt from the update still occurs. maybe use DEBIAN_FRONTEND=noninteractive ?
sudo apt-get -y install openjdk-8-jdk-headless
sleep 1 
mkdir /home/ubuntu/server
sleep 1 
echo "=== Starting setup for Spark ==="
sleep 1 
# download Spark
wget -c https://www-us.apache.org/dist/spark/spark-2.4.4/spark-2.4.4-bin-hadoop2.7.tgz -O spark-2.4.4-bin-hadoop2.7.tgz
sleep 1 
tar -xzf spark-2.4.4-bin-hadoop2.7.tgz
sleep 1 
mv spark-2.4.4-bin-hadoop2.7/ spark
sleep 1 
sudo mv spark/ /usr/lib/
sleep 1 
echo "=== Configuring Spark ==="
sleep 1 
# configure Spark
cp /usr/lib/spark/conf/spark-env.sh.template /usr/lib/spark/conf/spark-env.sh 
sleep 1 
cat >> /usr/lib/spark/conf/spark-env.sh << EOF
JAVA_HOME=/usr/lib/jvm/java-8-openjdk-amd64
SPARK_WORKER_MEMORY=4g
PYSPARK_PYTHON=python3
./bin/pyspark
EOF
sleep 1 
chmod a+rwx /usr/lib/spark/conf/spark-env.sh
sleep 1 
echo "=== Downloading hadoop==="
sleep 1 
wget -O /home/ubuntu/server/hadoop-2.8.5.tar.gz http://apache.mirrors.tds.net/hadoop/common/hadoop-2.8.5/hadoop-2.8.5.tar.gz
sleep 1 
tar xvzf /home/ubuntu/server/hadoop-2.8.5.tar.gz -C /home/ubuntu/server
sleep 1 
echo "=== Hadoop set up ==="
# this line edits the hadoop-env.sh and replace the JAVA_HOME line
sleep 1 
sed -i '25s/.*/export JAVA_HOME\=\/usr\/lib\/jvm\/java-8-openjdk-amd64/' /home/ubuntu/server/hadoop-2.8.5/etc/hadoop/hadoop-env.sh
sleep 1 
mkdir /home/ubuntu/server/hadoop-2.8.5/logs
sleep 1 
chmod -R 757 /home/ubuntu/server/hadoop-2.8.5
sleep 1 
# install pyspark
sudo mkdir -p /usr/local/hadoop/hdfs/data
sleep 1 
sudo chown -R ubuntu:ubuntu /usr/local/hadoop/hdfs/data
sleep 1 
sudo chmod 777 -R ubuntu /usr/local/hadoop/
sleep 1 
sudo apt-get install -y python3-pip
sleep 1 
pip3 install pyspark --no-cache-dir
sleep 1 
pip3 install pymongo --no-cache-dir
sleep 1 
pip3 install numpy --no-cache-dir
sleep 1 
# install sbt
echo "deb https://dl.bintray.com/sbt/debian /" | sudo tee -a /etc/apt/sources.list.d/sbt.list
sleep 1 
sudo apt-key adv --keyserver hkp://keyserver.ubuntu.com:80 --recv 2EE0EA64E40A89B84B2DF73499E82A75642AC823
sleep 1 
sudo apt-get -y install sbt
sleep 1 
# env for spark and hadoop
echo "=== Set env and PATH ==="
sleep 1 
echo "export JAVA_HOME=/usr/lib/jvm/java-8-openjdk-amd64" >> /etc/profile
sleep 1 
echo "export SBT_HOME=/usr/share/sbt-launcher-packaging/bin/sbt-launch.jar" >> /etc/profile
sleep 1 
echo "export SPARK_HOME=/usr/lib/spark" >> /etc/profile
sleep 1 
echo "export HADOOP_HOME=/home/ubuntu/server/hadoop-2.8.5" >> /etc/profile
sleep 1 
echo "export HADOOP_CONF_DIR=/home/ubuntu/server/hadoop-2.8.5/etc/hadoop" >> /etc/profile
sleep 1 
echo "export HADOOP_MAPRED_HOME=/home/ubuntu/server/hadoop-2.8.5" >> /etc/profile
sleep 1 
echo "export HADOOP_COMMON_HOME=/home/ubuntu/server/hadoop-2.8.5" >> /etc/profile
sleep 1 
echo "export HADOOP_HDFS_HOME=/home/ubuntu/server/hadoop-2.8.5" >> /etc/profile
sleep 1 
echo "export HADOOP_YARN_HOME=/home/ubuntu/server/hadoop-2.8.5" >> /etc/profile
sleep 1 
echo "export PATH=$PATH:$JAVA_HOME/bin:$SBT_HOME/bin:$SPARK_HOME/bin:$SPARK_HOME/sbin:/home/ubuntu/server/hadoop-2.8.5/bin" >> /etc/profile
sleep 1 
echo "=== Completed Spark Setup ==="
sleep 1 
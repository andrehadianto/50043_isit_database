#!/usr/bin/env bash

# $1 namenode dns, $2,$3,$4,$5,$6,$7,$8 datanode ip
sudo rm /home/ubuntu/server/hadoop-2.8.5/etc/hadoop/hdfs-site.xml
sleep 1 
sudo touch /home/ubuntu/server/hadoop-2.8.5/etc/hadoop/hdfs-site.xml
sleep 1 
sudo chmod a+rwx /home/ubuntu/server/hadoop-2.8.5/etc/hadoop/hdfs-site.xml
sleep 1 
cat >> /home/ubuntu/server/hadoop-2.8.5/etc/hadoop/hdfs-site.xml << EOF 
<?xml version="1.0" encoding="UTF-8"?>
<?xml-stylesheet type="text/xsl" href="configuration.xsl"?>

<configuration>
  <property>
    <name>dfs.replication</name>
    <value>3</value>
  </property>
  <property>
    <name>dfs.datanode.data.dir</name>
    <value>file:///usr/local/hadoop/hdfs/data</value>
  </property>
</configuration>
EOF
sleep 1 
sudo rm /home/ubuntu/server/hadoop-2.8.5/etc/hadoop/core-site.xml
sleep 1 
sudo touch /home/ubuntu/server/hadoop-2.8.5/etc/hadoop/core-site.xml
sleep 1 
sudo chmod a+rwx /home/ubuntu/server/hadoop-2.8.5/etc/hadoop/core-site.xml
sleep 1 
cat >> /home/ubuntu/server/hadoop-2.8.5/etc/hadoop/core-site.xml << EOF 
<?xml version="1.0" encoding="UTF-8"?>
<?xml-stylesheet type="text/xsl" href="configuration.xsl"?>

<configuration>
  <property>
    <name>fs.defaultFS</name>
    <value>hdfs://$1:9000</value>
  </property>
</configuration>
EOF


sleep 1 
touch /usr/lib/spark/conf/slaves
sleep 1
echo $1 >> /usr/lib/spark/conf/slaves
sleep 1  
echo $2 >> /usr/lib/spark/conf/slaves
sleep 1 
echo $3 >> /usr/lib/spark/conf/slaves
sleep 1 
echo $4 >> /usr/lib/spark/conf/slaves
sleep 1 
echo $5 >> /usr/lib/spark/conf/slaves
sleep 1 
echo $6 >> /usr/lib/spark/conf/slaves
sleep 1 
echo $7 >> /usr/lib/spark/conf/slaves
sleep 1 
echo $8 >> /usr/lib/spark/conf/slaves
sleep 1 
sudo mkdir -p /usr/local/hadoop/hdfs/data
sleep 1 
sudo chown -R ubuntu:ubuntu /usr/local/hadoop/hdfs/data
sleep 1
sudo apt-get install -y python3-pip
sleep 1
pip3 install numpy
sleep 1
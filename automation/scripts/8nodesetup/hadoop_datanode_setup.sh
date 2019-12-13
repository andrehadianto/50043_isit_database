#!/usr/bin/env bash

# $1 namenode dns, $2,$3,$4,$5,$6,$7,$8 datanode ip
sudo rm /home/ubuntu/server/hadoop-2.8.5/etc/hadoop/hdfs-site.xml
sudo touch /home/ubuntu/server/hadoop-2.8.5/etc/hadoop/hdfs-site.xml
sudo chmod a+rwx /home/ubuntu/server/hadoop-2.8.5/etc/hadoop/hdfs-site.xml
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

sudo rm /home/ubuntu/server/hadoop-2.8.5/etc/hadoop/core-site.xml
sudo touch /home/ubuntu/server/hadoop-2.8.5/etc/hadoop/core-site.xml
sudo chmod a+rwx /home/ubuntu/server/hadoop-2.8.5/etc/hadoop/core-site.xml
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

touch /usr/lib/spark/conf/slaves
echo $2 >> /usr/lib/spark/conf/slaves
echo $3 >> /usr/lib/spark/conf/slaves
echo $4 >> /usr/lib/spark/conf/slaves
echo $5 >> /usr/lib/spark/conf/slaves
echo $6 >> /usr/lib/spark/conf/slaves
echo $7 >> /usr/lib/spark/conf/slaves
echo $8 >> /usr/lib/spark/conf/slaves

sudo mkdir -p /usr/local/hadoop/hdfs/data
sudo chown -R ubuntu:ubuntu /usr/local/hadoop/hdfs/data
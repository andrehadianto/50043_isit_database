#!/usr/bin/env bash
#Note $1 is absolute AWS keypath, $2 is NameNode, $3 is SlaveNode1, $4 slavenode2, $5 slavenode3                                                                                hadoop_1_all.sh                                                                                  Modified  

rm /home/ubuntu/server/hadoop-2.8.5/etc/hadoop/core-site.xml
cat >> /home/ubuntu/server/hadoop-2.8.5/etc/hadoop/core-site.xml << EOF 
<?xml version="1.0" encoding="UTF-8"?>
<?xml-stylesheet type="text/xsl" href="configuration.xsl"?>

<configuration>
  <property>
    <name>fs.defaultFS</name>
    <value>$2:9000</value>
  </property>
</configuration>
EOF

sudo mkdir -p /usr/local/hadoop/hdfs/data
sudo chown -R ubuntu:ubuntu /usr/local/hadoop/hdfs/data

ssh-keygen -t rsa -f /home/ubuntu/.ssh/id_rsa -q -P "" 

cat /home/ubuntu/.ssh/id_rsa.pub | ssh -o StrictHostKeyChecking=no -i /home/ubuntu/$1 ubuntu@$2 "cat >> /home/ubuntu/.ssh/authorized_keys"

cat /home/ubuntu/.ssh/id_rsa.pub | ssh -o StrictHostKeyChecking=no -i /home/ubuntu/$1 ubuntu@$3 "cat >> /home/ubuntu/.ssh/authorized_keys"

cat >> /home/ubuntu/.ssh/config << EOF
Host nnode
  HostName $2
  User ubuntu
  IdentityFile ~/.ssh/id_rsa
 
Host dnode1
  HostName $3
  User ubuntu
  IdentityFile ~/.ssh/id_rsa
 
EOF


#  setup hdfs properties
rm /home/ubuntu/server/hadoop-2.8.5/etc/hadoop/hdfs-site.xml
cat >> /home/ubuntu/server/hadoop-2.8.5/etc/hadoop/hdfs-site.xml << EOF 
<?xml version="1.0" encoding="UTF-8"?>
<?xml-stylesheet type="text/xsl" href="configuration.xsl"?>

<configuration>
  <property>
    <name>dfs.replication</name>
    <value>3</value>
  </property>
  <property>
    <name>dfs.namenode.name.dir</name>
    <value>file:///usr/local/hadoop/hdfs/data</value>
  </property>
</configuration>
EOF


#  setup mapred properties
rm -f /home/ubuntu/server/hadoop-2.8.5/etc/hadoop/mapred-site.xmlec2-54-255-220-37.ap-southeast-1.compute.amazonaws.com: Host key verification failed.

cat >> /home/ubuntu/server/hadoop-2.8.5/etc/hadoop/mapred-site.xml << EOF 
<?xml version="1.0" encoding="UTF-8"?>
<?xml-stylesheet type="text/xsl" href="configuration.xsl"?>

<configuration>
  <property>
    <name>mapreduce.jobtracker.address</name>
    <value>$2:54311</value>
  </property>
  <property>
    <name>mapreduce.framework.name</name>
    <value>yarn</value>
  </property>
</configuration>
EOF

#  setup yarn properties
rm /home/ubuntu/server/hadoop-2.8.5/etc/hadoop/yarn-site.xml
cat >> /home/ubuntu/server/hadoop-2.8.5/etc/hadoop/yarn-site.xml << EOF 
<?xml version="1.0" encoding="UTF-8"?>
<?xml-stylesheet type="text/xsl" href="configuration.xsl"?>

<configuration>
  <property>
    <name>yarn.nodemanager.aux-services</name>
    <value>mapreduce_shuffle</value>
  </property>
  <property>
    <name>yarn.nodemanager.aux-services.mapreduce.shuffle.class</name>
    <value>org.apache.hadoop.mapred.ShuffleHandler</value>
  </property>
  <property>
    <name>yarn.resourcemanager.hostname</name>
    <value>$2</value>
  </property>
</configuration>
EOF

#  setup master and slaves
rm -f /home/ubuntu/server/hadoop-2.8.5/etc/hadoop/masters
cat >> /home/ubuntu/server/hadoop-2.8.5/etc/hadoop/masters << EOF
$2
EOF
# need to make it vary depending on arg oso because your no of dnode changes.
rm  /home/ubuntu/server/hadoop-2.8.5/etc/hadoop/slaves
cat >> /home/ubuntu/server/hadoop-2.8.5/etc/hadoop/slaves << EOF
$3
EOF

yes | /bin/bash /home/ubuntu/start_hadoop_cluster.sh 





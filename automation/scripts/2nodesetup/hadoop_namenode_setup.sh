#!/usr/bin/env bash
#Note $1 is absolute AWS keypath, $2 is NameNode dns, $3 is SlaveNode dns, $4 is slavenode ip

echo "Changing config files..."
# change core-site.xml
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
    <value>hdfs://$2:9000</value>
  </property>
</configuration>
EOF
sleep 1

sudo mkdir -p /usr/local/hadoop/hdfs/data
sleep 1
sudo chown -R ubuntu:ubuntu /usr/local/hadoop/hdfs/data
sleep 1

# passwordless ssh
ssh-keygen -t rsa -f /home/ubuntu/.ssh/id_rsa -q -P ""
sleep 1

cat /home/ubuntu/.ssh/id_rsa.pub | ssh -o StrictHostKeyChecking=no -i $1 ubuntu@$2 "cat >> /home/ubuntu/.ssh/authorized_keys"
sleep 1

cat /home/ubuntu/.ssh/id_rsa.pub | ssh -o StrictHostKeyChecking=no -i $1 ubuntu@$3 "cat >> /home/ubuntu/.ssh/authorized_keys"
sleep 1

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
sleep 1
#  setup hdfs properties
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
    <name>dfs.namenode.name.dir</name>
    <value>file:///usr/local/hadoop/hdfs/data</value>
  </property>
</configuration>
EOF
sleep 1

#  setup mapred properties
sudo rm /home/ubuntu/server/hadoop-2.8.5/etc/hadoop/mapred-site.xml
sleep 1
sudo touch /home/ubuntu/server/hadoop-2.8.5/etc/hadoop/mapred-site.xml
sleep 1
sudo chmod a+rwx /home/ubuntu/server/hadoop-2.8.5/etc/hadoop/mapred-site.xml
sleep 1
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
sleep 1
#  setup yarn properties
sudo rm /home/ubuntu/server/hadoop-2.8.5/etc/hadoop/yarn-site.xml
sleep 1
sudo touch /home/ubuntu/server/hadoop-2.8.5/etc/hadoop/yarn-site.xml
sleep 1
sudo chmod a+rwx /home/ubuntu/server/hadoop-2.8.5/etc/hadoop/yarn-site.xml
sleep 1
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
sleep 1
#  setup master and slaves
sudo rm /home/ubuntu/server/hadoop-2.8.5/etc/hadoop/masters
sleep 1
sudo touch /home/ubuntu/server/hadoop-2.8.5/etc/hadoop/masters
sleep 1
sudo chmod a+rwx /home/ubuntu/server/hadoop-2.8.5/etc/hadoop/masters
sleep 1
cat >> /home/ubuntu/server/hadoop-2.8.5/etc/hadoop/masters << EOF
$2
EOF
sleep 1

sudo rm /home/ubuntu/server/hadoop-2.8.5/etc/hadoop/slaves
sleep 1
sudo touch /home/ubuntu/server/hadoop-2.8.5/etc/hadoop/slaves
sleep 1
sudo chmod a+rwx /home/ubuntu/server/hadoop-2.8.5/etc/hadoop/slaves
sleep 1
cat >> /home/ubuntu/server/hadoop-2.8.5/etc/hadoop/slaves << EOF
$3
EOF
sleep 1
touch /usr/lib/spark/conf/slaves
sleep 1
echo $4 >> /usr/lib/spark/conf/slaves
sleep 1

# install mongo/mysql/numpy (needed to get data and run pyspark script)
echo "Installing Mongo..."
{
    wget -qO - https://www.mongodb.org/static/pgp/server-4.2.asc | sudo apt-key add -
    sleep 1
    echo "deb [ arch=amd64 ] https://repo.mongodb.org/apt/ubuntu bionic/mongodb-org/4.2 multiverse" | sudo tee /etc/apt/sources.list.d/mongodb-org-4.2.list
    sleep 1
    sudo apt-get update
    sleep 1
    sudo apt-get install -y mongodb-org
    sleep 1
} || {
    echo "ERROR: installing mongodb"
    sleep 1
}

{
    sudo service mongod start
    sleep 1
} || {
    sudo systemctl enable mongod
    sleep 1
    sudo service mongod start
    sleep 1
}

sudo apt install -y mysql-server-5.7
sleep 1
sudo apt-get install -y python3-pip
sleep 1
pip3 install numpy
sleep 1
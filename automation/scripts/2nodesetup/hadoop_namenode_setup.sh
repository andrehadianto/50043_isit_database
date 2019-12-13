#!/usr/bin/env bash
#Note $1 is absolute AWS keypath, $2 is NameNode dns, $3 is SlaveNode dns, $4 is slavenode ip

echo "arguments are $1 $2 $3 $4"
echo "Changing config files..."

sudo rm /home/ubuntu/server/hadoop-2.8.5/etc/hadoop/core-site.xml
sudo touch /home/ubuntu/server/hadoop-2.8.5/etc/hadoop/core-site.xml
sudo chmod a+rwx /home/ubuntu/server/hadoop-2.8.5/etc/hadoop/core-site.xml
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

sudo mkdir -p /usr/local/hadoop/hdfs/data
sudo chown -R ubuntu:ubuntu /usr/local/hadoop/hdfs/data

ssh-keygen -t rsa -f /home/ubuntu/.ssh/id_rsa -q -P ""


cat /home/ubuntu/.ssh/id_rsa.pub | ssh -o StrictHostKeyChecking=no -i $1 ubuntu@$2 "cat >> /home/ubuntu/.ssh/authorized_keys"

cat /home/ubuntu/.ssh/id_rsa.pub | ssh -o StrictHostKeyChecking=no -i $1 ubuntu@$3 "cat >> /home/ubuntu/.ssh/authorized_keys"


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
    <name>dfs.namenode.name.dir</name>
    <value>file:///usr/local/hadoop/hdfs/data</value>
  </property>
</configuration>
EOF


#  setup mapred properties
sudo rm /home/ubuntu/server/hadoop-2.8.5/etc/hadoop/mapred-site.xml
sudo touch /home/ubuntu/server/hadoop-2.8.5/etc/hadoop/mapred-site.xml
sudo chmod a+rwx /home/ubuntu/server/hadoop-2.8.5/etc/hadoop/mapred-site.xml
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
sudo rm /home/ubuntu/server/hadoop-2.8.5/etc/hadoop/yarn-site.xml
sudo touch /home/ubuntu/server/hadoop-2.8.5/etc/hadoop/yarn-site.xml
sudo chmod a+rwx /home/ubuntu/server/hadoop-2.8.5/etc/hadoop/yarn-site.xml
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
sudo rm /home/ubuntu/server/hadoop-2.8.5/etc/hadoop/masters
sudo touch /home/ubuntu/server/hadoop-2.8.5/etc/hadoop/masters
sudo chmod a+rwx /home/ubuntu/server/hadoop-2.8.5/etc/hadoop/masters
cat >> /home/ubuntu/server/hadoop-2.8.5/etc/hadoop/masters << EOF
$2
EOF
# need to make it vary depending on arg oso because your no of dnode changes.
sudo rm /home/ubuntu/server/hadoop-2.8.5/etc/hadoop/slaves
sudo touch /home/ubuntu/server/hadoop-2.8.5/etc/hadoop/slaves
sudo chmod a+rwx /home/ubuntu/server/hadoop-2.8.5/etc/hadoop/slaves
cat >> /home/ubuntu/server/hadoop-2.8.5/etc/hadoop/slaves << EOF
$3
EOF

touch /usr/lib/spark/conf/slaves
echo $4 >> /usr/lib/spark/conf/slaves

# install sqoop
echo "=== Set Up for SQOOP === "
echo "Installing Apache Sqoop 1.4.7..."
wget https://www-us.apache.org/dist/sqoop/1.4.7/sqoop-1.4.7.bin__hadoop-2.6.0.tar.gz
tar -zxvf sqoop-1.4.7.bin__hadoop-2.6.0.tar.gz
sudo mv sqoop-1.4.7.bin__hadoop-2.6.0 /usr/lib
sudo chmod -R 757 /usr/lib/sqoop-1.4.7.bin__hadoop-2.6.0

export SQOOP_HOME=/usr/lib/sqoop-1.4.7.bin__hadoop-2.6.0
export PATH=$PATH:$SQOOP_HOME/bin
export SQOOP_CONF_DIR=$SQOOP_HOME/conf

echo "Installing JDBC driver..."
wget http://dev.mysql.com/get/Downloads/Connector-J/mysql-connector-java-5.1.38.tar.gz
tar -xvzf mysql-connector-java-5.1.38.tar.gz
sudo cp mysql-connector-java-5.1.38/mysql-connector-java-5.1.38-bin.jar $SQOOP_HOME/lib/

sudo chmod a+rw /etc/profile

echo "export SQOOP_HOME=/usr/lib/sqoop-1.4.7.bin__hadoop-2.6.0" >> /etc/profile
echo "export PATH=$PATH:$SQOOP_HOME/bin" >> /etc/profile
echo "export SQOOP_CONF_DIR=$SQOOP_HOME/conf" >> /etc/profile

echo "Installing Mongo..."
# download mongo
{
    wget -qO - https://www.mongodb.org/static/pgp/server-4.2.asc | sudo apt-key add -
    echo "deb [ arch=amd64 ] https://repo.mongodb.org/apt/ubuntu bionic/mongodb-org/4.2 multiverse" | sudo tee /etc/apt/sources.list.d/mongodb-org-4.2.list
    sudo apt-get update
    sudo apt-get install -y mongodb-org
} || {
    # catch
    echo "ERROR: installing mongodb"
}

{
    sudo service mongod start
} || {
    sudo systemctl enable mongod
    sudo service mongod start
}

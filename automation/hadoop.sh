#!/bin/bash

# update yum
sudo yum update

# install java-1.7.0 and java-1.8.0 (is not a typo)
sudo yum install java-1.8.0-openjdk-devel
y
sudo yum install java-1.8.0-openjdk-devel
y

# download and extract hadoop
wget http://apache.mirrors.tds.net/hadoop/common/hadoop-2.8.5/hadoop-2.8.5.tar.gz -P ~/Downloads
sudo tar zxvf ~/Downloads/hadoop-* -C /usr/local
sudo mv /usr/local/hadoop-* /usr/local/hadoop

# configure variables
cat >> .bashrc << EOF
export HADOOP_HOME=/usr/local/hadoop
export PATH=\$PATH:\$HADOOP_HOME/bin
export HADOOP_CONF_DIF=\$HADOOP_HOME/etc/hadoop
                                                                                        
# Set JAVA_HOME                                                                         
export JAVA_HOME=/usr/lib/jvm/java-1.8.0-openjdk
export PATH=\$PATH:\$JAVA_HOME/bin
EOF

# run
source ~/.bashrc
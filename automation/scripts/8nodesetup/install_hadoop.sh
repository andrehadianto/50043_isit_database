#!/usr/bin/env bash

sudo apt-get -y update 
# The prompt from the update still occurs. maybe use DEBIAN_FRONTEND=noninteractive ?
sudo apt-get -y install openjdk-8-jdk-headless
mkdir /home/ubuntu/server
wget -O /home/ubuntu/server/hadoop-2.8.5.tar.gz http://apache.mirrors.tds.net/hadoop/common/hadoop-2.8.5/hadoop-2.8.5.tar.gz
tar xvzf /home/ubuntu/server/hadoop-2.8.5.tar.gz -C /home/ubuntu/server
#this line edits the hadoop-env.sh and replace the JAVA_HOME line
sed -i '25s/.*/export JAVA_HOME\=\/usr\/lib\/jvm\/java-8-openjdk-amd64/' /home/ubuntu/server/hadoop-2.8.5/etc/hadoop/hadoop-env.sh


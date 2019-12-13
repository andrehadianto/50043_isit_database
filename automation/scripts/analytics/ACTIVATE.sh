#!/usr/bin/env bash

echo "Putting stuff on hdfs..."
/home/ubuntu/server/hadoop-2.8.5/bin/hadoop fs -mkdir /data
/home/ubuntu/server/hadoop-2.8.5/bin/hadoop fs -put /home/ubuntu/meta.json /data/meta.json
/home/ubuntu/server/hadoop-2.8.5/bin/hadoop fs -put /home/ubuntu/kindle.csv /data/kindle.csv

# install the spark scripts
echo "Getting spark scripts..."
wget -c https://www.dropbox.com/s/c59ejvagf5ng5ta/correlation.py?dl=0 -O correlation.py
wget -c https://www.dropbox.com/s/b7k2hps5fte1ka0/tfidf.py?dl=0 -O tfidf.py

# run the spark scripts
echo "Running spark scripts..."
/home/ubuntu/server/hadoop-2.8.5/bin/hadoop fs -rm -r /corr
/home/ubuntu/server/hadoop-2.8.5/bin/hadoop fs -rm -r /tfidf
MASTER_IP=$(curl ifconfig.co)
export MASTER_IP
echo $MASTER_IP
/usr/lib/spark/bin/spark-submit --master spark://$MASTER_IP:7077 tfidf.py $MASTER_IP
/usr/lib/spark/bin/spark-submit --master spark://$MASTER_IP:7077 correlation.py $MASTER_IP

echo "===============================COMPLETE================================="
#!/usr/bin/env bash

hadoop fs -mkdir /data
hadoop fs -put /home/ubuntu/meta.json /data/meta.json
hadoop fs -put /home/ubuntu/kindle.csv /data/kindle.csv

# install the spark scripts
wget -c https://www.dropbox.com/s/vri7r6vnpsq283y/correlation.py?dl=0 -O correlation.py
wget -c https://www.dropbox.com/s/av3312z4qk9iuj3/tfidf.py?dl=0 -O tfidf.py

# run the spark scripts
MASTER_IP=$(curl ifconfig.co)
export MASTER_IP
$SPARK_HOME/bin/spark-submit --master spark://$MASTER_IP:7077 tfidf.py $MASTER_IP
$SPARK_HOME/bin/spark-submit --master spark://$MASTER_IP:7077 correlation.py $MASTER_IP
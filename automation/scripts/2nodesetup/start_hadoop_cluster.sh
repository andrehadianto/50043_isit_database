#!/usr/bin/env bash

# start hadoop
yes | /bin/bash /home/ubuntu/server/hadoop-2.8.5/bin/hdfs namenode -format
sleep 1
ssh -o StrictHostKeyChecking=no 0.0.0.0 "exit"
sleep 1
/bin/bash /home/ubuntu/server/hadoop-2.8.5/sbin/start-dfs.sh
sleep 1
yes | /bin/bash /home/ubuntu/server/hadoop-2.8.5/sbin/start-yarn.sh
sleep 1
yes | /bin/bash /home/ubuntu/server/hadoop-2.8.5/sbin/mr-jobhistory-daemon.sh start historyserver
sleep 1
# start spark
/usr/lib/spark/sbin/start-master.sh
sleep 1
LOCAL_PUBLIC_IP=$(curl ifconfig.co)
sleep 1
export LOCAL_PUBLIC_IP
sleep 1
ssh dnode1 "/bin/bash /usr/lib/spark/sbin/start-slave.sh spark://$1:7077"
sleep 1
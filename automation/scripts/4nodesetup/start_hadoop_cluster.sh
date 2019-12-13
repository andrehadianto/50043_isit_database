#!/usr/bin/env bash

yes | /bin/bash /home/ubuntu/server/hadoop-2.8.5/bin/hdfs namenode -format
ssh -o StrictHostKeyChecking=no 0.0.0.0 "exit"
/bin/bash /home/ubuntu/server/hadoop-2.8.5/sbin/start-dfs.sh
yes | /bin/bash /home/ubuntu/server/hadoop-2.8.5/sbin/start-yarn.sh
yes | /bin/bash /home/ubuntu/server/hadoop-2.8.5/sbin/mr-jobhistory-daemon.sh start historyserver

/usr/lib/spark/sbin/start-master.sh
LOCAL_PUBLIC_IP=$(curl ifconfig.co)
export LOCAL_PUBLIC_IP
/usr/lib/spark/sbin/start-slave.sh spark://$LOCAL_PUBLIC_IP:7077
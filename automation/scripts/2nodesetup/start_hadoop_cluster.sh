#!/usr/bin/env bash

yes | /bin/bash /home/ubuntu/server/hadoop-2.8.5/bin/hdfs namenode -format #Might want to add a feedback to inform setupfailed if it fails
ssh -o StrictHostKeyChecking=no 0.0.0.0 "exit"
/bin/bash /home/ubuntu/server/hadoop-2.8.5/sbin/start-dfs.sh   
yes | /bin/bash /home/ubuntu/server/hadoop-2.8.5/sbin/start-yarn.sh 
yes | /bin/bash /home/ubuntu/server/hadoop-2.8.5/sbin/mr-jobhistory-daemon.sh start historyserver 


#!/usr/bin/env bash

/bin/bash /home/ubuntu/server/hadoop-2.8.5/bin/hdfs namenode -format #Might want to add a feedback to inform setupfailed if it fails
/bin/bash /home/ubuntu/server/hadoop-2.8.5/sbin/start-dfs.sh 
/bin/bash /home/ubuntu/server/hadoop-2.8.5/sbin/start-yarn.sh 
/bin/bash /home/ubuntu/server/hadoop-2.8.5/sbin/mr-jobhistory-daemon.sh start historyserver 


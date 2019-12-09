#!/usr/bin/env bash
# $1 AWS key path, $2 namenode dns, $3 datanode dns
scp -o StrictHostKeyChecking=no -i $1 $1  ubuntu@$2:/home/ubuntu/$1
#scp -o StrictHostKeyChecking=no -i $1 "install_hadoop.sh"  ubuntu@$2:/home/ubuntu/install_hadoop.sh
scp -o StrictHostKeyChecking=no -i $1 "hadoop_namenode_setup_2node.sh"  ubuntu@$2:/home/ubuntu/hadoop_namenode_setup_2node.sh
scp -o StrictHostKeyChecking=no -i $1 "start_hadoop_cluster.sh"  ubuntu@$2:/home/ubuntu/start_hadoop_cluster.sh

#Run datanode setup first arg is namenode dns
#Test this line first
#scp -o StrictHostKeyChecking=no -i $1 "install_hadoop.sh"  ubuntu@$3:/home/ubuntu/install_hadoop.sh
scp -o StrictHostKeyChecking=no -i $1 "hadoop_datanode_setup.sh"  ubuntu@$3:/home/ubuntu/hadoop_datanode_setup.sh
#ssh -o StrictHostKeyChecking=no -i $1 ubuntu@$3 "chmod +x /home/ubuntu/install_hadoop.sh"
ssh -o StrictHostKeyChecking=no -i $1 ubuntu@$3 "chmod +x /home/ubuntu/hadoop_datanode_setup.sh"
ssh -o StrictHostKeyChecking=no -i $1 ubuntu@$3 "/bin/bash  /home/ubuntu/install_hadoop.sh"
ssh -o StrictHostKeyChecking=no -i $1 ubuntu@$3 "/bin/bash  /home/ubuntu/hadoop_datanode_setup.sh $2" 
 
#Run namenode setup and everything else should run
#ssh -o StrictHostKeyChecking=no -i $1 ubuntu@$2 "chmod +x /home/ubuntu/install_hadoop.sh"
ssh -o StrictHostKeyChecking=no -i $1 ubuntu@$2 "chmod +x /home/ubuntu/hadoop_namenode_setup_2node.sh"
ssh -o StrictHostKeyChecking=no -i $1 ubuntu@$2 "chmod +x /home/ubuntu/start_hadoop_cluster.sh"
#ssh -o StrictHostKeyChecking=no -i $1 ubuntu@$2 "/bin/bash /home/ubuntu/install_hadoop.sh"
ssh -o StrictHostKeyChecking=no -i $1 ubuntu@$2 "/bin/bash /home/ubuntu/hadoop_namenode_setup_2node.sh $1 $2 $3"


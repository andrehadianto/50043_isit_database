#!/usr/bin/env bash
# $1 AWS key path, $2 namenode dns, $3,$4,$5 datanode dns
scp -o StrictHostKeyChecking=no -i $1 $1  ubuntu@$2:/home/ubuntu/aws_key.pem
ssh -o StrictHostKeyChecking=no -i $1 ubuntu@$2 "chmod 400 /home/ubuntu/aws_key.pem"
scp -o StrictHostKeyChecking=no -i $1 "hadoop_namenode_setup_4node.sh"  ubuntu@$2:/home/ubuntu/hadoop_namenode_setup.sh
scp -o StrictHostKeyChecking=no -i $1 "start_hadoop_cluster.sh"  ubuntu@$2:/home/ubuntu/start_hadoop_cluster.sh

#Run datanode setup first arg is namenode dns
#Test this line first
scp -o StrictHostKeyChecking=no -i $1 "hadoop_datanode_setup.sh"  ubuntu@$3:/home/ubuntu/hadoop_datanode_setup.sh
ssh -o StrictHostKeyChecking=no -i $1 ubuntu@$3 "chmod +x /home/ubuntu/hadoop_datanode_setup.sh"
ssh -o StrictHostKeyChecking=no -i $1 ubuntu@$3 "/bin/bash  /home/ubuntu/hadoop_datanode_setup.sh $2" 

scp -o StrictHostKeyChecking=no -i $1 "hadoop_datanode_setup.sh"  ubuntu@$4:/home/ubuntu/hadoop_datanode_setup.sh
ssh -o StrictHostKeyChecking=no -i $1 ubuntu@$4 "chmod +x /home/ubuntu/hadoop_datanode_setup.sh"
ssh -o StrictHostKeyChecking=no -i $1 ubuntu@$4 "/bin/bash  /home/ubuntu/hadoop_datanode_setup.sh $2" 

scp -o StrictHostKeyChecking=no -i $1 "hadoop_datanode_setup.sh"  ubuntu@$5:/home/ubuntu/hadoop_datanode_setup.sh
ssh -o StrictHostKeyChecking=no -i $1 ubuntu@$5 "chmod +x /home/ubuntu/hadoop_datanode_setup.sh"
ssh -o StrictHostKeyChecking=no -i $1 ubuntu@$5 "/bin/bash  /home/ubuntu/hadoop_datanode_setup.sh $2" 

#Run namenode setup and everything else should run
ssh -o StrictHostKeyChecking=no -i $1 ubuntu@$2 "chmod +x /home/ubuntu/hadoop_namenode_setup.sh"
ssh -o StrictHostKeyChecking=no -i $1 ubuntu@$2 "chmod +x /home/ubuntu/start_hadoop_cluster.sh"
ssh -o StrictHostKeyChecking=no -i $1 ubuntu@$2 "/bin/bash /home/ubuntu/hadoop_namenode_setup.sh /home/ubuntu/aws_key.pem $2 $3 $4 $5"

ssh -o StrictHostKeyChecking=no -i $1 ubuntu@$2 "/bin/bash /home/ubuntu/start_hadoop_cluster.sh"

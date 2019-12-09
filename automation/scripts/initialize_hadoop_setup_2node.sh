#!/usr/bin/env bash
# $1 AWS key path, $2 namenode dns, $3,$4,$5 datanode dns
echo "Preparing namenode and datanode..."
scp -o StrictHostKeyChecking=no -i $1 $1  ubuntu@$2:/home/ubuntu/key.pem
scp -o StrictHostKeyChecking=no -i $1 "scripts/hadoop_namenode_setup_2node.sh"  ubuntu@$2:/home/ubuntu/hadoop_namenode_setup_2node.sh
scp -o StrictHostKeyChecking=no -i $1 "scripts/start_hadoop_cluster.sh"  ubuntu@$2:/home/ubuntu/start_hadoop_cluster.sh

#Run datanode setup first arg is namenode dns
scp -o StrictHostKeyChecking=no -i $1 "scripts/hadoop_datanode_setup.sh"  ubuntu@$3:/home/ubuntu/hadoop_datanode_setup.sh
ssh -o StrictHostKeyChecking=no -i $1 ubuntu@$3 "chmod +x /home/ubuntu/hadoop_datanode_setup.sh"
ssh -o StrictHostKeyChecking=no -i $1 ubuntu@$3 "/bin/bash  /home/ubuntu/hadoop_datanode_setup.sh $2" 
 
#Run namenode setup and everything else should run
ssh -o StrictHostKeyChecking=no -i $1 ubuntu@$2 "chmod +x /home/ubuntu/hadoop_namenode_setup_2node.sh"
ssh -o StrictHostKeyChecking=no -i $1 ubuntu@$2 "chmod +x /home/ubuntu/start_hadoop_cluster.sh"
ssh -o StrictHostKeyChecking=no -i $1 ubuntu@$2 "/bin/bash /home/ubuntu/hadoop_namenode_setup_2node.sh key.pem $2 $3"

echo "Just a little longer..."

ssh -o StrictHostKeyChecking=no -i $1 ubuntu@$2 "/home/ubuntu/start_hadoop_cluster.sh"

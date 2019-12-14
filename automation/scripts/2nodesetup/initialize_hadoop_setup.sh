#!/usr/bin/env bash
# $1 AWS key path, $2 namenode dns, $3 datanode dns, $4 datanode ip
echo "Preparing namenode and datanode..."
sleep 1
scp -o StrictHostKeyChecking=no -i $1 $1  ubuntu@$2:/home/ubuntu/aws_key.pem
sleep 1
ssh -o StrictHostKeyChecking=no -i $1 ubuntu@$2 "chmod 400 /home/ubuntu/aws_key.pem"
sleep 1
scp -o StrictHostKeyChecking=no -i $1 "scripts/2nodesetup/hadoop_namenode_setup.sh" ubuntu@$2:/home/ubuntu/hadoop_namenode_setup.sh
sleep 1
scp -o StrictHostKeyChecking=no -i $1 "scripts/2nodesetup/start_hadoop_cluster.sh" ubuntu@$2:/home/ubuntu/start_hadoop_cluster.sh
sleep 1

#Run datanode setup first arg is namenode dns
#Test this line first
scp -o StrictHostKeyChecking=no -i $1 "scripts/2nodesetup/hadoop_datanode_setup.sh"  ubuntu@$3:/home/ubuntu/hadoop_datanode_setup.sh
sleep 1
ssh -o StrictHostKeyChecking=no -i $1 ubuntu@$3 "chmod +x /home/ubuntu/hadoop_datanode_setup.sh"
sleep 1
ssh -o StrictHostKeyChecking=no -i $1 ubuntu@$3 "/bin/bash /home/ubuntu/hadoop_datanode_setup.sh $2 $4"
sleep 1

#Run namenode setup and everything else should run
ssh -o StrictHostKeyChecking=no -i $1 ubuntu@$2 "chmod +x /home/ubuntu/hadoop_namenode_setup.sh"
sleep 1
ssh -o StrictHostKeyChecking=no -i $1 ubuntu@$2 "chmod +x /home/ubuntu/start_hadoop_cluster.sh"
sleep 1
ssh -o StrictHostKeyChecking=no -i $1 ubuntu@$2 "/bin/bash /home/ubuntu/hadoop_namenode_setup.sh /home/ubuntu/aws_key.pem $2 $3 $4"
sleep 1

echo "Just a little longer..."

ssh -o StrictHostKeyChecking=no -i $1 ubuntu@$2 "/bin/bash /home/ubuntu/start_hadoop_cluster.sh"
sleep 1

echo "Hdfs is up! Please visit $2:50070"
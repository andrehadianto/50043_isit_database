#!/usr/bin/env bash
# $1 AWS key path, $2 namenode dns, $3,$4,$5 datanode dns
echo "Preparing namenode and datanode..."
scp -o StrictHostKeyChecking=no -i $1 $1  ubuntu@$2:/home/ubuntu/aws_key.pem
ssh -o StrictHostKeyChecking=no -i $1 ubuntu@$2 "chmod 400 /home/ubuntu/aws_key.pem"
scp -o StrictHostKeyChecking=no -i $1 "hadoop_namenode_setup_8node.sh"  ubuntu@$2:/home/ubuntu/hadoop_namenode_setup.sh
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

scp -o StrictHostKeyChecking=no -i $1 "hadoop_datanode_setup.sh"  ubuntu@$6:/home/ubuntu/hadoop_datanode_setup.sh
ssh -o StrictHostKeyChecking=no -i $1 ubuntu@$6 "chmod +x /home/ubuntu/hadoop_datanode_setup.sh"
ssh -o StrictHostKeyChecking=no -i $1 ubuntu@$6 "/bin/bash  /home/ubuntu/hadoop_datanode_setup.sh $2" 
 
scp -o StrictHostKeyChecking=no -i $1 "hadoop_datanode_setup.sh"  ubuntu@$7:/home/ubuntu/hadoop_datanode_setup.sh
ssh -o StrictHostKeyChecking=no -i $1 ubuntu@$7 "chmod +x /home/ubuntu/hadoop_datanode_setup.sh"
ssh -o StrictHostKeyChecking=no -i $1 ubuntu@$7 "/bin/bash  /home/ubuntu/hadoop_datanode_setup.sh $2" 

scp -o StrictHostKeyChecking=no -i $1 "hadoop_datanode_setup.sh"  ubuntu@$8:/home/ubuntu/hadoop_datanode_setup.sh
ssh -o StrictHostKeyChecking=no -i $1 ubuntu@$8 "chmod +x /home/ubuntu/hadoop_datanode_setup.sh"
ssh -o StrictHostKeyChecking=no -i $1 ubuntu@$8 "/bin/bash  /home/ubuntu/hadoop_datanode_setup.sh $2" 

scp -o StrictHostKeyChecking=no -i $1 "hadoop_datanode_setup.sh"  ubuntu@$9:/home/ubuntu/hadoop_datanode_setup.sh
ssh -o StrictHostKeyChecking=no -i $1 ubuntu@$9 "chmod +x /home/ubuntu/hadoop_datanode_setup.sh"
ssh -o StrictHostKeyChecking=no -i $1 ubuntu@$9 "/bin/bash  /home/ubuntu/hadoop_datanode_setup.sh $2" 

#Run namenode setup and everything else should run
ssh -o StrictHostKeyChecking=no -i $1 ubuntu@$2 "chmod +x /home/ubuntu/hadoop_namenode_setup.sh"
ssh -o StrictHostKeyChecking=no -i $1 ubuntu@$2 "chmod +x /home/ubuntu/start_hadoop_cluster.sh"
ssh -o StrictHostKeyChecking=no -i $1 ubuntu@$2 "/bin/bash /home/ubuntu/hadoop_namenode_setup.sh /home/ubuntu/aws_key.pem $2 $3 $4 $5 $6 $7 $8 $9"

echo "Just a little longer..."

ssh -o StrictHostKeyChecking=no -i $1 ubuntu@$2 "/bin/bash /home/ubuntu/start_hadoop_cluster.sh"

echo "Hdfs is up! Please visit $2:5000"
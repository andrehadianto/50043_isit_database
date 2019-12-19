#!/usr/bin/env bash
auto_retry_scp(){
    arg1=$1
    until $arg1; do
        echo "Try again on $2..."
        sleep 5
    done
}

auto_retry_ssh(){
    arg1=$1
    arg2=$2
    arg2=$3
    until $arg1 "$arg2"; do
        echo "Try again on $3..."
        sleep 5
    done
}

auto_retry_scp "scp -o StrictHostKeyChecking=no -i $1 $1  ubuntu@$2:/home/ubuntu/aws_key.pem" "SCP pemkey name node"
auto_retry ssh "ssh -o StrictHostKeyChecking=no -i $1 ubuntu@$2" "chmod 400 /home/ubuntu/aws_key.pem" "SSH name node"
auto_retry_scp "scp -o StrictHostKeyChecking=no -i $1 hadoop_namenode_setup.sh  ubuntu@$2:/home/ubuntu/hadoop_namenode_setup.sh" "SCP namenodeSetupScript name node"
auto_retry_scp "scp -o StrictHostKeyChecking=no -i $1 start_hadoop_cluster.sh  ubuntu@$2:/home/ubuntu/start_hadoop_cluster.sh" "SCP starthadoopcluster name node"

#Run datanode setup first arg is namenode dns
#Test this line first
auto_retry_scp "scp -o StrictHostKeyChecking=no -i $1 hadoop_datanode_setup.sh  ubuntu@$3:/home/ubuntu/hadoop_datanode_setup.sh" "SCP copying hadoop datanode setup 1"
auto_retry_ssh "ssh -o StrictHostKeyChecking=no -i $1 ubuntu@$3" "chmod +x /home/ubuntu/hadoop_datanode_setup.sh" "SSH chmod the setup file 1"
auto_retry_ssh "ssh -o StrictHostKeyChecking=no -i $1 ubuntu@$3" "/bin/bash  /home/ubuntu/hadoop_datanode_setup.sh $2" "SSH running setup file 1"

auto_retry_scp "scp -o StrictHostKeyChecking=no -i $1 hadoop_datanode_setup.sh  ubuntu@$4:/home/ubuntu/hadoop_datanode_setup.sh" "SCP copying hadoop datanode setup 2"
auto_retry_ssh "ssh -o StrictHostKeyChecking=no -i $1 ubuntu@$4" "chmod +x /home/ubuntu/hadoop_datanode_setup.sh" "SSH chmod the setup file 2"
auto_retry_ssh "ssh -o StrictHostKeyChecking=no -i $1 ubuntu@$4" "/bin/bash  /home/ubuntu/hadoop_datanode_setup.sh $2" "SSH running setup file 2"

auto_retry_scp "scp -o StrictHostKeyChecking=no -i $1 hadoop_datanode_setup.sh  ubuntu@$5:/home/ubuntu/hadoop_datanode_setup.sh" "SCP copying hadoop datanode setup 3"
auto_retry_ssh "ssh -o StrictHostKeyChecking=no -i $1 ubuntu@$5" "chmod +x /home/ubuntu/hadoop_datanode_setup.sh" "SSH chmod the setup file 3"
auto_retry_ssh "ssh -o StrictHostKeyChecking=no -i $1 ubuntu@$5" "/bin/bash  /home/ubuntu/hadoop_datanode_setup.sh $2" "SSH running setup file 3"

auto_retry_ssh "ssh -o StrictHostKeyChecking=no -i $1 ubuntu@$2" "chmod +x /home/ubuntu/hadoop_namenode_setup.sh" "SSH chmod the namenode setup file"
auto_retry_ssh "ssh -o StrictHostKeyChecking=no -i $1 ubuntu@$2" "chmod +x /home/ubuntu/start_hadoop_cluster.sh" "SSH chmod the hadoop cluster file"
auto_retry_ssh "ssh -o StrictHostKeyChecking=no -i $1 ubuntu@$2" "/bin/bash /home/ubuntu/hadoop_namenode_setup.sh /home/ubuntu/aws_key.pem $2 $3 $4 $5" "SSH running namenode_setup script"



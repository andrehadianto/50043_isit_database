#!/usr/bin/env bash
# $1 AWS key path, $2 namenode dns, $3,$4,$5 datanode dns
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

auto_retry_scp "scp -o StrictHostKeyChecking=no -i $1 hadoop_datanode_setup.sh  ubuntu@$4:/home/ubuntu/hadoop_datanode_setup.sh" "SCP copying hadoop datanode setup 1"
auto_retry_ssh "ssh -o StrictHostKeyChecking=no -i $1 ubuntu@$4" "chmod +x /home/ubuntu/hadoop_datanode_setup.sh" "SSH chmod the setup file 1"
auto_retry_ssh "ssh -o StrictHostKeyChecking=no -i $1 ubuntu@$4" "/bin/bash  /home/ubuntu/hadoop_datanode_setup.sh $2" "SSH running setup file 1"

auto_retry_scp "scp -o StrictHostKeyChecking=no -i $1 hadoop_datanode_setup.sh  ubuntu@$5:/home/ubuntu/hadoop_datanode_setup.sh" "SCP copying hadoop datanode setup 1"
auto_retry_ssh "ssh -o StrictHostKeyChecking=no -i $1 ubuntu@$5" "chmod +x /home/ubuntu/hadoop_datanode_setup.sh" "SSH chmod the setup file 1"
auto_retry_ssh "ssh -o StrictHostKeyChecking=no -i $1 ubuntu@$5" "/bin/bash  /home/ubuntu/hadoop_datanode_setup.sh $2" "SSH running setup file 1"

auto_retry_scp "scp -o StrictHostKeyChecking=no -i $1 hadoop_datanode_setup.sh  ubuntu@$6:/home/ubuntu/hadoop_datanode_setup.sh" "SCP copying hadoop datanode setup 1"
auto_retry_ssh "ssh -o StrictHostKeyChecking=no -i $1 ubuntu@$6" "chmod +x /home/ubuntu/hadoop_datanode_setup.sh" "SSH chmod the setup file 1"
auto_retry_ssh "ssh -o StrictHostKeyChecking=no -i $1 ubuntu@$6" "/bin/bash  /home/ubuntu/hadoop_datanode_setup.sh $2" "SSH running setup file 1"

auto_retry_scp "scp -o StrictHostKeyChecking=no -i $1 hadoop_datanode_setup.sh  ubuntu@$7:/home/ubuntu/hadoop_datanode_setup.sh" "SCP copying hadoop datanode setup 1"
auto_retry_ssh "ssh -o StrictHostKeyChecking=no -i $1 ubuntu@$7" "chmod +x /home/ubuntu/hadoop_datanode_setup.sh" "SSH chmod the setup file 1"
auto_retry_ssh "ssh -o StrictHostKeyChecking=no -i $1 ubuntu@$7" "/bin/bash  /home/ubuntu/hadoop_datanode_setup.sh $2" "SSH running setup file 1"

auto_retry_scp "scp -o StrictHostKeyChecking=no -i $1 hadoop_datanode_setup.sh  ubuntu@$8:/home/ubuntu/hadoop_datanode_setup.sh" "SCP copying hadoop datanode setup 1"
auto_retry_ssh "ssh -o StrictHostKeyChecking=no -i $1 ubuntu@$8" "chmod +x /home/ubuntu/hadoop_datanode_setup.sh" "SSH chmod the setup file 1"
auto_retry_ssh "ssh -o StrictHostKeyChecking=no -i $1 ubuntu@$8" "/bin/bash  /home/ubuntu/hadoop_datanode_setup.sh $2" "SSH running setup file 1"

auto_retry_scp "scp -o StrictHostKeyChecking=no -i $1 hadoop_datanode_setup.sh  ubuntu@$9:/home/ubuntu/hadoop_datanode_setup.sh" "SCP copying hadoop datanode setup 1"
auto_retry_ssh "ssh -o StrictHostKeyChecking=no -i $1 ubuntu@$9" "chmod +x /home/ubuntu/hadoop_datanode_setup.sh" "SSH chmod the setup file 1"
auto_retry_ssh "ssh -o StrictHostKeyChecking=no -i $1 ubuntu@$9" "/bin/bash  /home/ubuntu/hadoop_datanode_setup.sh $2" "SSH running setup file 1"


#Run namenode setup and everything else should run
auto_retry_ssh "ssh -o StrictHostKeyChecking=no -i $1 ubuntu@$2" "chmod +x /home/ubuntu/hadoop_namenode_setup.sh" "SSH chmod the namenode setup file"
auto_retry_ssh "ssh -o StrictHostKeyChecking=no -i $1 ubuntu@$2" "chmod +x /home/ubuntu/start_hadoop_cluster.sh" "SSH chmod the hadoop cluster file"
auto_retry_ssh "ssh -o StrictHostKeyChecking=no -i $1 ubuntu@$2" "/bin/bash /home/ubuntu/hadoop_namenode_setup.sh /home/ubuntu/aws_key.pem $2 $3 $4 $5 $6 $7 $8 $9" "SSH running namenode_setup script"



auto_retry_ssh "ssh -o StrictHostKeyChecking=no -i $1 ubuntu@$2" "/bin/bash /home/ubuntu/start_hadoop_cluster.sh"

#!/usr/bin/env bash
# $1 AWS key path, $2 namenode dns, $3 datanode dns, $4 datanode ip
echo "Preparing namenode and datanode..."

auto_retry_scp(){
    arg1=$1
    until $arg1; do
        echo "Try again..."
        sleep 5
    done
}

auto_retry_ssh(){
    arg1=$1
    arg2=$2
    until $arg1 "$arg2"; do
        echo "Try again..."
        sleep 5
    done
}

auto_retry_scp "scp -o StrictHostKeyChecking=no -i $1 $1  ubuntu@$2:/home/ubuntu/aws_key.pem"
sleep 1
auto_retry_ssh "ssh -o StrictHostKeyChecking=no -i $1 ubuntu@$2" "chmod 400 /home/ubuntu/aws_key.pem"
sleep 1
auto_retry_scp "scp -o StrictHostKeyChecking=no -i $1 scripts/2nodesetup/hadoop_namenode_setup.sh ubuntu@$2:/home/ubuntu/hadoop_namenode_setup.sh"
sleep 1
auto_retry_scp "scp -o StrictHostKeyChecking=no -i $1 scripts/2nodesetup/start_hadoop_cluster.sh ubuntu@$2:/home/ubuntu/start_hadoop_cluster.sh"
sleep 1


auto_retry_scp "scp -o StrictHostKeyChecking=no -i $1 scripts/2nodesetup/hadoop_datanode_setup.sh ubuntu@$3:/home/ubuntu/hadoop_datanode_setup.sh"
sleep 1
auto_retry_ssh "ssh -o StrictHostKeyChecking=no -i $1 ubuntu@$3" "chmod +x /home/ubuntu/hadoop_datanode_setup.sh"
sleep 1
auto_retry_ssh "ssh -o StrictHostKeyChecking=no -i $1 ubuntu@$3" "/bin/bash /home/ubuntu/hadoop_datanode_setup.sh $2 $4"
sleep 1


auto_retry_ssh "ssh -o StrictHostKeyChecking=no -i $1 ubuntu@$2" "chmod +x /home/ubuntu/hadoop_namenode_setup.sh"
sleep 1
auto_retry_ssh "ssh -o StrictHostKeyChecking=no -i $1 ubuntu@$2" "chmod +x /home/ubuntu/start_hadoop_cluster.sh"
sleep 1
auto_retry_ssh "ssh -o StrictHostKeyChecking=no -i $1 ubuntu@$2" "/bin/bash /home/ubuntu/hadoop_namenode_setup.sh /home/ubuntu/aws_key.pem $2 $3 $4"
sleep 1

echo "Just a little longer..."

auto_retry_ssh "ssh -o StrictHostKeyChecking=no -i $1 ubuntu@$2" "/bin/bash /home/ubuntu/start_hadoop_cluster.sh $2"
sleep 1

echo "Hdfs is up! Please visit $2:50070"
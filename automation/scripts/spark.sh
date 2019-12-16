#!/bin/bash

echo "=== Starting setup for Spark ==="
# download Spark
wget -c https://www-us.apache.org/dist/spark/spark-2.4.4/spark-2.4.4-bin-hadoop2.7.tgz -O spark-2.4.4-bin-hadoop2.7.tgz
tar -xzf spark-2.4.4-bin-hadoop2.7.tgz
mv spark-2.4.4-bin-hadoop2.7/ spark
sudo mv spark/ /usr/lib/


echo "=== Configuring Spark ==="
# configure Spark
cp /usr/lib/spark/conf/spark-env.sh.template /usr/lib/spark/conf/spark-env.sh 

cat >> /usr/lib/spark/conf/spark-env.sh << EOF
JAVA_HOME=/usr/lib/jvm/java-11-openjdk-amd64
SPARK_WORKER_MEMORY=4g
PYSPARK_PYTHON=python3
./bin/pyspark
EOF

echo "=== Installing Java ==="
# install java
sudo apt-get -y update
sudo apt install -y default-jre
sudo apt install -y default-jdk

sudo apt-get install -y python3-pip
pip3 install pyspark --no-cache-dir
pip3 install pymongo --no-cache-dir

# install sbt
echo "deb https://dl.bintray.com/sbt/debian /" | sudo tee -a /etc/apt/sources.list.d/sbt.list
sudo apt-key adv --keyserver hkp://keyserver.ubuntu.com:80 --recv 2EE0EA64E40A89B84B2DF73499E82A75642AC823
sudo apt-get -y install sbt

source ~/.bashrc

echo "=== Editing bashrc ==="
cat >> ~/.bashrc << EOF
export JAVA_HOME=/usr/lib/jvm/java-11-openjdk-amd64
export SBT_HOME=/usr/share/sbt-launcher-packaging/bin/sbt-launch.jar
export SPARK_HOME=/usr/lib/spark
export PATH=$PATH:$JAVA_HOME/bin
export PATH=$PATH:$SBT_HOME/bin:$SPARK_HOME/bin:$SPARK_HOME/sbin
EOF

source ~/.bashrc
exec bash

echo "=== Completed Spark Setup ==="
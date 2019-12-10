#!/bin/bash

echo "=== Set Up for PyMongo-Spark === "

echo "Setting up Mongo Java Driver..."
sudo apt install openjdk-9-jre
sudo apt install -y openjdk-9-jdk

git clone https://github.com/mongodb/mongo-java-driver.git
cd mongo-java-driver
./gradlew check # mongod must be running with enableTestCommands; --setParameter enableTestCommands=1 for this to work
echo "Mongo Java Driver installed"

echo "Setting up Mongo Hadoop connector..."
# EITHER download mongo-hadoop jar
wget http://repo1.maven.org/maven2/org/mongodb/mongo-hadoop/mongo-hadoop-spark/1.5.1/ -O $HADOOP_PREFIX/lib/mongo-hadoop-spark-1.5.1/

git clone https://github.com/mongodb/mongo-hadoop.git

# # OR build Mongo Hadoop connector
# cd mongo-hadoop
# ./gradlew jar
# # copy built jar files to /lib in each cluster node
# cp -a /source/. $HADOOP_PREFIX/lib/mongo-hadoop-spark-1.5.1/

echo "Installing PyMongo-Spark..."
# download and install pymongo-spark
cd mongo-hadoop/spark/src/main/python
python setup.py install

# install pymongo on each machine of Spark cluster
# ---> add pymongo to requirements.txt
cd ../../../../../../
python -m pip install pymongo

echo "Edit CLASSPATH and PYTHONPATH..."
# put mongo-hadoop-spark.jar in Spark's CLASSPATH
# https://spark.apache.org/docs/latest/
bin/pyspark --jars mongo-hadoop-spark-1.5.1.jar \
            --driver-class-path mongo-hadoop-spark.jar

# add pymongo-spark to Spark's PYTHONPATH
# EDIT
bin/pyspark --py-files /path/to/pymongo_spark.py,/path/to/pymongo.egg

# cd $SPARK_HOME
# bin/pyspark --jars /path/to/mongo-hadoop-spark.jar \
#          --driver-class-path /path/to/mongo-hadoop-spark.jar \
#          --py-files /path/to/pymongo_spark.py,/path/to/pymongo.egg

echo "Connecting to mongoDB..."
# run mongo_spark.py to create RDD
cd $SPARK_HOME
export PYTHONPATH=$PYTHONPATH:/path/to/pymongo_spark.py/directory
./bin/spark-submit --jars /path/to/mongo-hadoop-spark.jar \
          --driver-class-path /path/to/mongo-hadoop-spark.jar \
          mongo_spark.py
# EDIT

echo "=== Finished connecting Mongo to HDFS ==="
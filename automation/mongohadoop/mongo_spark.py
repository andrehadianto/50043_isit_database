from pyspark import SparkContext
import pymongo_spark

pymongo_spark.activate()

# read from mongoDB
rdd = sc.mongoRDD('mongodb://localhost:27017/db.collection')
# rdd.first()   
# rdd.count()
# https://hackersandslackers.com/working-with-pyspark-rdds/

# write to mongo
# only can write to empty collection
rdd.saveToMongoDB('mongodb://host_ip:port/db.collection')
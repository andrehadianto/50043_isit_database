import math
import sys
import pyspark
from pyspark.sql.functions import *
from pyspark.sql.functions import length
from pyspark.sql import SparkSession

# to run
# $SPARK_HOME/bin/spark-submit --master spark://<master-ip>:7077 correlation.py <master-ip>
# $SPARK_HOME/bin/spark-submit --master spark://ec2-54-169-135-228.ap-southeast-1.compute.amazonaws.com:7077 correlation.py ec2-54-169-135-228.ap-southeast-1.compute.amazonaws.com


sc = pyspark.SparkContext("spark://{}:7077".format(sys.argv[1]), "corr")
spark = SparkSession(sc)

# ================
# Preprocessing
# ================

reviews_df = spark.read.csv("hdfs://{}:9000/data/{}".format(sys.argv[1], "kindle.csv"), header=True, sep=",")
# get id, asin and reviewText columns from reviews dataset
reviews = reviews_df.select("id", "asin", "reviewText")
# convert reviewText -> length of review
reviews = reviews.withColumn("reviewText", length(reviews.reviewText))
# get average review length (group by asin)
reviews_avg = reviews.groupBy("asin").agg(mean("reviewText").alias("average_reviewLength"))


meta_df = spark.read.json("hdfs://{}:9000/data/{}".format(sys.argv[1], "meta.json"))
prices = meta_df.select("asin", "price")
# join by asin
data = reviews_avg.join(prices, ["asin"])


# ==================

data = data.select("price", "average_reviewLength")
data = data.filter(col("price").isNotNull() & col("average_reviewLength").isNotNull())		# drop None values
n = data.count()

data = data.rdd.map(list)

flatdata = data.flatMap(lambda row: (
	("x", row[0]),
	("y", row[1]),
	("x2", row[0] * row[0]),
	("y2", row[1] * row[1]),
	("xy", row[0] * row[1])))

# Sort by key so that we will get an order we can slice from
reduced_data = flatdata.reduceByKey(lambda x,y: x+y).sortByKey()

# Retrieving our terms required for calculating the correlation
end_data = reduced_data.take(5)
x = end_data[0][1]
xx = end_data[1][1]
xy = end_data[2][1]
y = end_data[3][1]
yy = end_data[4][1]

numerator = xy - (x * y)/n
denominator = math.sqrt(xx - (x * x)/n) * math.sqrt(yy - (y * y)/n)
correlation = numerator / denominator
print("The Pearson Correlation between average review length and price is: ")
print(correlation)

# create a rdd so that we can save
output = sc.parallelize(['Correlation', correlation])
output.saveAsTextFile("hdfs://{}:9000/corr".format(sys.argv[1]))
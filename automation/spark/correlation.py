import math
import sys
import pyspark
from pyspark.sql.functions import *
from pyspark.sql.functions import length

# Uncomment when Hadoop is set up
# sc = pyspark.SparkContext("spark://{}:7077".format(sys.argv[1]), "corr")
# spark = SparkSession(sc)
# reviews_df = sc.textFile(sys.argv[2])			# need to change this accordingly
# meta_df = sc.textFile(sys.argv[3])			# need to change this accordingly

# ================
# Preprocessing
# ================

# Currently reading from local file
reviews_df = spark.read.csv("C:/Users/User/Desktop/SUTD/Term 6/50.043 Database and Big Data Systems/project/kindle-reviews/kindle_short.csv", header=True, sep=",")
# get _c0, asin and reviewText columns from reviews dataset
reviews = reviews_df.select("_c0", "asin", "reviewText")
# convert reviewText -> length of review
reviews = reviews.withColumn("reviewText", length(reviews.reviewText))
# get average review length (group by asin)
reviews_avg = reviews.groupBy("asin").agg(mean("reviewText").alias("average_reviewLength"))
# get price
meta_df = spark.read.json('C:/Users/User/Desktop/SUTD/Term 6/50.043 Database and Big Data Systems/project/meta_kindle_store/meta_short.json')
prices = meta_df.select("asin", "price")
# join by asin
data = reviews_avg.join(prices, ["asin"])


# ==================

n = data.count()
data = data.select("price", "average_reviewLength")
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
# output = sc.parallelize(['Correlation', correlation])
# output.saveAsTextFile("hdfs://{}:9000/corr".format(sys.argv[1]))
import sys
import pyspark
from pyspark.sql import SparkSession
from pyspark.ml.feature import CountVectorizer, IDF, Tokenizer
from pyspark.sql.functions import udf, col
from pyspark.sql.types import StringType

# to run
# $SPARK_HOME/bin/spark-submit --master spark://<master-ip>:7077 tfidf.py <master-ip>
# $SPARK_HOME/bin/spark-submit --master spark://ec2-54-169-135-228.ap-southeast-1.compute.amazonaws.com:7077 tfidf.py ec2-54-169-135-228.ap-southeast-1.compute.amazonaws.com


sc = pyspark.SparkContext("spark://{}:7077".format(sys.argv[1]), "tfidf")
spark = SparkSession(sc)

data = spark.read.csv("hdfs://{}:9000/data/{}".format(sys.argv[1], "kindle.csv"), header=True, sep=",")

# drop rows with null values in reviews
data = data.na.drop(subset=["reviewText"])

# convert to words
tokenizer = Tokenizer(inputCol="reviewText", outputCol="words")
wordsData = tokenizer.transform(data)


# use CountVectorizer to get term frequency vectors
cv = CountVectorizer(inputCol="words", outputCol="rawFeatures", vocabSize=20)
model = cv.fit(wordsData)
featurizedData = model.transform(wordsData)

vocab = model.vocabulary

# Applying IDF needs two passes:
# First to compute the IDF vector and second to scale the term frequencies by IDF.
idf = IDF(inputCol="rawFeatures", outputCol="features")
idfModel = idf.fit(featurizedData)
rescaledData = idfModel.transform(featurizedData)


# trying to map the index of word -> actual word cause CountVectorizer gives index
def map_to_word1(row, vocab):
    d = {}
    array = row.toArray()
    for i in range(len(row)):
        # if it is 0 -> ignore, else change the key to corresponding word
        if (array[i] != 0):
            tfidf = array[i]
            word = vocab[i]
            d[word] = tfidf
    return str(d)

def map_to_word(vocab):
    return udf(lambda row: map_to_word1(row, vocab))

# apply udf to convert index back to word
df = rescaledData.withColumn("tfidf", map_to_word(vocab)(rescaledData.features))

output = df.select("id", "tfidf")
output.write.format("csv").save("hdfs://{}:9000/tfidf".format(sys.argv[1]))
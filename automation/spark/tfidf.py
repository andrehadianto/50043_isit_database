import sys
import pyspark
from pyspark.sql import SparkSession
from pyspark.ml.feature import CountVectorizer, IDF, Tokenizer
from pyspark.sql.functions import udf, col
from pyspark.sql.types import StringType

# uncomment when Hadoop is set up
# sc = pyspark.SparkContext("spark://{}:7077".format(sys.argv[1]), "tfidf")
# data = spark.read.csv("data.csv", header=True, sep=",")
# spark = SparkSession(sc)

data = spark.read.csv("C:/Users/User/Desktop/SUTD/Term 6/50.043 Database and Big Data Systems/project/kindle-reviews/kindle_short.csv", 
    header=True, sep=",")

# convert to words
tokenizer = Tokenizer(inputCol="reviewText", outputCol="words")
wordsData = tokenizer.transform(data)

# use CountVectorizer to get term frequency vectors
cv = CountVectorizer(inputCol="words", outputCol="rawFeatures")
model = cv.fit(wordsData)
featurizedData = model.transform(wordsData)

vocab = model.vocabulary

# Applying IDF needs two passes:
# First to compute the IDF vector and second to scale the term frequencies by IDF.
featurizedData.cache()
idf = IDF(inputCol="rawFeatures", outputCol="features")
idfModel = idf.fit(featurizedData)
rescaledData = idfModel.transform(featurizedData)
tfidf = rescaledData.select("features").collect()

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
df = rescaledData.withColumn("modified", map_to_word(vocab)(rescaledData.features))

# df.select("_c0", "modified").saveAsTextFile("hdfs://{}:9000/tfidf".format(sys.argv[1]))
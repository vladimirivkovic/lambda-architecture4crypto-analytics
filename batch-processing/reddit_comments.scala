import org.apache.spark.sql.SparkSession

// For implicit conversions like converting RDDs to DataFrames
import spark.implicits._
import org.apache.spark.sql.avro._

// val spark = SparkSession.builder().appName("Reddit comments example").getOrCreate()

val path = "hdfs://namenode:9000/user/data/subreddit-Bitcoin/"
val commentsDF = spark.read.format("avro").load(path)

commentsDF.printSchema()

commentsDF.createOrReplaceTempView("comments")

spark.sql("SELECT body FROM comments").show()

import org.apache.spark.sql.SparkSession

// For implicit conversions like converting RDDs to DataFrames
import spark.implicits._
import org.apache.spark.sql.avro._

// val spark = SparkSession.builder().appName("Exchange rates example").getOrCreate()

val path = "hdfs://namenode:9000/user/data/exchange-rates/"
val ratesDF = spark.read.format("avro").load(path)

ratesDF.printSchema()

ratesDF.createOrReplaceTempView("rates")

spark.sql("SELECT FROMSYMBOL, TOSYMBOL, avg(PRICE) FROM rates GROUP BY FROMSYMBOL, TOSYMBOL").show

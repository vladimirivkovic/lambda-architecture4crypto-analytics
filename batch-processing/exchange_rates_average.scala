import org.apache.spark.sql.SparkSession
import org.apache.spark.sql.types.DateType

// For implicit conversions like converting RDDs to DataFrames
import spark.implicits._
import org.apache.spark.sql.avro._

// val spark = SparkSession.builder().appName("Exchange rates example").getOrCreate()

val path = "hdfs://namenode:9000/user/data/exchange-rates/"
val ratesDF = spark.read.format("avro").load(path)

ratesDF.printSchema()
val filteredRatesDF = ratesDF.select("*").filter($"PRICE" > 0).filter($"LASTUPDATE" > 0)
filteredRatesDF.createOrReplaceTempView("rates")

spark.sql("SELECT FROMSYMBOL, TOSYMBOL, avg(PRICE) FROM rates GROUP BY FROMSYMBOL, TOSYMBOL").show

spark.sql("SELECT FROMSYMBOL, TOSYMBOL, PRICE, to_timestamp(LASTUPDATE) AS datetime FROM rates WHERE LASTUPDATE > 1591747200").show

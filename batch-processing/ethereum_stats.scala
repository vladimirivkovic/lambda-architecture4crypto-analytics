import org.apache.spark.sql.SparkSession

// For implicit conversions like converting RDDs to DataFrames
import spark.implicits._
import org.apache.spark.sql.avro._

// val spark = SparkSession.builder().appName("Gas average example").getOrCreate()

val path = "hdfs://namenode:9000/user/data/eth-block/"
val blocksDF = spark.read.format("avro").load(path)

// blocksDF.printSchema()

val ratesPath = "hdfs://namenode:9000/user/data/exchange-rates/"
val ratesDF = spark.read.format("avro").load(ratesPath)

// ratesDF.printSchema()
val filteredRatesDF = ratesDF.select("*").filter($"PRICE" > 0).filter($"LASTUPDATE" > 0)
filteredRatesDF.createOrReplaceTempView("rates")

blocksDF.createOrReplaceTempView("blocks")

// spark.sql("SELECT AVG(gasUsed) FROM blocks").show
// spark.sql("SELECT COUNT(*) FROM blocks").show
// spark.sql("SELECT COUNT(distinct miner) FROM blocks").show

blocksDF.withColumn("txs_no", size($"transactions")).agg(avg($"txs_no")).show

spark.sql("SELECT hash, to_timestamp(timestamp), avg(PRICE) FROM blocks JOIN rates " + 
          "ON bround(timestamp/60, 0) == bround(LASTUPDATE/60, 0) " + 
          "WHERE FROMSYMBOL == 'ETH' GROUP BY hash, timestamp ORDER BY timestamp").show

//.select("hash", to_timestamp($"timestamp"), "avg_price")
filteredRatesDF
    .filter($"FROMSYMBOL" === "ETH")
    .join(blocksDF, bround($"LASTUPDATE"/60) === bround($"timestamp"/60))
    .groupBy("hash", "timestamp")
    .agg(avg($"PRICE").alias("avg_price"))
    .orderBy("timestamp")
    .show

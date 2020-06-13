import org.apache.spark.sql.SparkSession

// For implicit conversions like converting RDDs to DataFrames
import spark.implicits._
import org.apache.spark.sql.avro._

// val spark = SparkSession.builder().appName("Gas average example").getOrCreate()

val path = "hdfs://namenode:9000/user/data/eth-block/"
val blocksDF = spark.read.format("avro").load(path)

blocksDF.printSchema()

blocksDF.createOrReplaceTempView("blocks")

spark.sql("SELECT AVG(gasUsed) FROM blocks").show

spark.sql("SELECT COUNT(*) FROM blocks").show

spark.sql("SELECT COUNT(distinct miner) FROM blocks").show

blocksDF.withColumn("txs_no", size($"transactions")).agg(avg($"txs_no")).show

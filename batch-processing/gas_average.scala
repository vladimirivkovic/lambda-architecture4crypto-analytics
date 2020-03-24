import spark.implicits._

val path = "hdfs://namenode:9000/user/data/ethereum/blocks-*.json"
val blocksDF = spark.read.json(path)

blocksDF.printSchema()

blocksDF.createOrReplaceTempView("blocks")

spark.sql("SELECT AVG(gasUsed) FROM blocks").show()

spark.sql("SELECT COUNT(*) FROM blocks").show()

spark.sql("SELECT COUNT(distinct miner) FROM blocks").show()

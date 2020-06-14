package myapps

import java.util.Properties
import java.util.concurrent.TimeUnit
 
import org.apache.kafka.streams.kstream.Materialized
import org.apache.kafka.streams.scala.ImplicitConversions._
import org.apache.kafka.streams.scala._
import org.apache.kafka.streams.scala.kstream._
import org.apache.kafka.streams.{KafkaStreams, StreamsConfig}
import org.apache.kafka.common.serialization.Serde
import play.api.libs.json.JsValue

import myapps.util._
 
object EthereumStats extends App {
  import Serdes._
 
  val props: Properties = {
    val p = new Properties()
    p.put(StreamsConfig.APPLICATION_ID_CONFIG, "ethstats-application")
    p.put(StreamsConfig.BOOTSTRAP_SERVERS_CONFIG, sys.env("KAFKA_BROKER"))
    p
  }

  implicit val jsonSerde: Serde[JsValue] = new JsonSerde
 
  val builder: StreamsBuilder = new StreamsBuilder
  val stream: KStream[String, JsValue] = builder.stream[String, JsValue]("eth-block")
  stream.foreach((key, value) => println(key + ", " + (value \ "hash").get))
 
  val streams: KafkaStreams = new KafkaStreams(builder.build(), props)
  streams.start()
 
  sys.ShutdownHookThread {
     streams.close(10, TimeUnit.SECONDS)
  }
}
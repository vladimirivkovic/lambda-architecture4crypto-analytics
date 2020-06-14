package myapps.util

import java.util

import org.apache.kafka.common.serialization.Serializer
import play.api.libs.json.{JsValue, Json}

/**
  * Convenient kafka serializer for play JsValue.
  */
class JsonSerializer extends Serializer[JsValue] {
  override def configure(configs: util.Map[String, _], isKey: Boolean): Unit = {}

  override def serialize(topic: String, data: JsValue): Array[Byte] =
    Json.stringify(data).getBytes("UTF8")

  override def close(): Unit = {}
}
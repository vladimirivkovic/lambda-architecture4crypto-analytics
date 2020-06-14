package myapps.util

import java.util

import org.apache.kafka.common.errors.SerializationException
import org.apache.kafka.common.serialization.Deserializer
import play.api.libs.json.{JsValue, Json}

/**
  * Convenient kafka deserializer for play JsValue.
  */
class JsonDeserializer extends Deserializer[JsValue] {
  override def configure(configs: util.Map[String, _], isKey: Boolean): Unit = {}

  override def deserialize(topic: String, data: Array[Byte]): JsValue =
    try {
      Json.parse(data)
    } catch {
      case e: Throwable =>
        throw new SerializationException("Failed to deserialize json data: " + e.getMessage)
    }

  override def close(): Unit = {}
}
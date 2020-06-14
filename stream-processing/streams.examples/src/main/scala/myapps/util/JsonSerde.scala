package myapps.util

import java.util

import org.apache.kafka.common.serialization._
import play.api.libs.json.JsValue


class JsonSerde extends Serde[JsValue] {
  override def deserializer(): Deserializer[JsValue] = new JsonDeserializer

  override def configure(configs: util.Map[String, _], isKey: Boolean): Unit = ()

  override def close(): Unit = ()

  override def serializer(): Serializer[JsValue] = new JsonSerializer
}
import paho.mqtt.client as mqtt
from waveBackend.settings import MQTT_HOST, MQTT_PORT, MQTT_QOS


# TODO: complete function
def send_message(path, msg):
    client = mqtt.Client("tmp_message_client")
    client.connect(MQTT_HOST, MQTT_PORT)
    client.publish(path, msg, qos=MQTT_QOS)

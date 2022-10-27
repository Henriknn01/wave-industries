import paho.mqtt.client as mqtt
import time
import datetime




# address of the mqtt broker connecting to the broker
mqttBroker = "10.22.186.196"
port = "1883"
client = mqtt.Client("Device")
client.connect(mqttBroker)

topic = "topic/hub"
message = "japanese salary man "


while True:
    ts = str(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    client.publish(topic, message + ts)
    print(message + ts)

    time.sleep(5)

import paho.mqtt.client as mqtt
import time

# address of the mqtt broker connecting to the broker
mqttBroker = "129.241.152.12"
port = "1883"
client = mqtt.Client("Device")
client.connect(mqttBroker)

while True:
    client.publish("TOPIC")
    print("Published" )

    time.sleep(10)

import paho.mqtt.client as mqtt
import time


# when data is reciever, prints out the datas payload
def on_message(client, data, message):
    print("Recieved data_ ", str(message.payload.decode("utf-8")))


# address of the mqtt broker
mqttBroker = "129.241.152.12"
port = "1883"
client = mqtt.Client("Device")
client.connect(mqttBroker)

# starts loop, subscribers to a topic. Prints out the payload of the topic subscribed.
client.loop_start()
client.subscribe("SUB")
client.on_message = on_message
time.sleep(30)
client.loop_stop()

# source: https://www.youtube.com/watch?v=kuyCd53AOtg
# documentation used: https://www.eclipse.org/paho/index.php?page=clients/python/index.php


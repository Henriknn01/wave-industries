import paho.mqtt.subscribe as subscribe
import time


def on_message_print(client, userdata, message):
    print("%s %s" % (message.topic, message.payload))


mqttBroker = "10.22.186.196"
subscribe.callback(on_message_print, "#", hostname=mqttBroker)
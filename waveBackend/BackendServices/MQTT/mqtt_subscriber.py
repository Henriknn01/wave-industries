import paho.mqtt.subscribe as subscribe
import time
import requests

# api address and key
API_ENDPOINT = ""
API_KEY = ""

# data to send to the api
data_to_API = {'ShipEngine/',
               'Date Received'}


# post to api
def on_message_forward(message):
    requests.post(url=API_ENDPOINT, data=message)


def on_message_print(client, userdata, message):
    print("%s %s" % (message.topic, message.payload))


mqttBroker = "79.160.34.197"
subscribe.callback(on_message_print, "#", hostname=mqttBroker)

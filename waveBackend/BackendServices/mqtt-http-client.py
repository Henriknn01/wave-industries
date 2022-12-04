from datetime import datetime

import paho.mqtt.client as mqtt
import requests

# Set client variables
CLIENT_ID = "vessel-name"  # Change to your preferred client id
BROKER_HOST = "next.0xbace.io"  # Change to your MQTT broker ip
BROKER_PORT = 1883
KEEP_ALIVE = 60

API_ENTRIES_URL = "http://127.0.0.1:8000/entries/"  # Change to your API entries endpoint
API_STREAMS_URL = "http://127.0.0.1:8000/mqtt-streams/"  # Change to your API stream endpoint

topics = []

# TODO: implement logging


def get_topics():
    """
    Gets the topics available in the api and adds them to the topic list.
    """
    r = requests.get(API_STREAMS_URL+"?format=json")
    response_list = r.json()
    for topic in response_list["results"]:
        topics.append(topic["mqtt_path"])


def post_message(msg, topic):
    """
    Post http message to REST API with specified message and topic.
    :param msg: message
    :param topic: mqtt topic
    """
    data = {
        "data": msg,
        "timestamp": datetime.now().isoformat(),  # TODO: get timestamp from mqtt message?
        "stream": topic
    }
    r = requests.post(API_ENTRIES_URL+"?format=json", data=data)
    if r.status_code != 201:
        # If the REST API responds with anything other than status code 201, print an error message.
        print(f"error sending message, error code: {r.status_code}")


def on_connect(client, userdata, flags, rc):
    """
    On connect to the MQTT broker subscribe to topics in the topic list.
    """
    print(f"{CLIENT_ID} successfully connected to {BROKER_HOST} - {datetime.utcnow()}")
    print(f"connected with code: {rc}")
    # Subscribe
    for topic in topics:
        client.subscribe(topic, 2)
        print(f"subscribed to topic: {topic}")


def on_message(client, userdata, msg):
    """
    On MQTT message received posts mqtt message to REST API.

    :param client: MQTT client
    :param userdata: user data
    :param msg: MQTT message
    """
    # TODO: fix timestamp
    # USED FOR DEBUG:
    # print(f"Message received [{msg.topic}] - {datetime.fromtimestamp(msg.timestamp)}: {msg.payload.decode()} ")
    post_message(msg.payload.decode(), msg.topic)


if __name__ == "__main__":
    get_topics()
    mclient = mqtt.Client(CLIENT_ID)
    mclient.on_connect = on_connect
    mclient.on_message = on_message
    mclient.connect(BROKER_HOST, BROKER_PORT, KEEP_ALIVE)
    mclient.loop_forever()

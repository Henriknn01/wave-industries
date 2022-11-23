from datetime import datetime

import paho.mqtt.client as mqtt
import requests

CLIENT_ID = "vessel-name"
BROKER_HOST = "79.160.34.197"
BROKER_PORT = 1883
KEEP_ALIVE = 60

API_ENTRIES_URL = "http://127.0.0.1:8000/entries/"
API_STREAMS_URL = "http://127.0.0.1:8000/mqtt-streams/"

topics = []


def get_topics():
    r = requests.get(API_STREAMS_URL+"?format=json")
    response_list = r.json()
    for topic in response_list:
        topics.append(topic["mqtt_path"])


def post_message(msg, topic):
    data = {
        "data": msg,
        "timestamp": datetime.now().timestamp(),
        "stream": topic
    }
    r = requests.post(API_ENTRIES_URL+"?format=json", data=data)
    if r.status_code != 201:
        print(f"error sending message, error code: {r.status_code}")


def on_connect(client, userdata, flags, rc):
    print(f"{CLIENT_ID} successfully connected to {BROKER_HOST} - {datetime.utcnow()}")
    print(f"connected with code: {rc}")
    # Subscribe
    for topic in topics:
        client.subscribe(topic, 2)
        print(f"subscribed to topic: {topic}")


def on_message(client, userdata, msg):
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

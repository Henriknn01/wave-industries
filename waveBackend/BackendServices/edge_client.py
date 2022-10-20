import paho.mqtt.client as mqtt

CLIENT_ID = "vessel-name"
BROKER_HOST = "test.mosquitto.org"
BROKER_PORT = 1883
KEEP_ALIVE = 60

sensors = ["engine-1-fuel", "engine-2-fuel", ]


def on_connect():
    pass


def on_message():
    pass


def publish(mqtt_client):
    for s in sensors:
        sensor_data = 0
        client.publish(f"{CLIENT_ID}/{s}/", sensor_data)


def subscribe():
    pass


if __name__ == "__main__":
    client = mqtt.Client(CLIENT_ID)
    client.connect(BROKER_HOST, BROKER_PORT, KEEP_ALIVE)
    client.on_connect = on_connect
    client.on_message = on_message
    client.loop_start()
    while True:
        publish(client)

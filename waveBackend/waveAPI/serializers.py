from .models import Ship, MqttStream, Entry
from rest_framework import serializers


class ShipSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Ship
        fields = ['name', 'identifier']


class MqttStreamSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = MqttStream
        fields = ['ship', 'mqtt_path']


class EntrySerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Entry
        fields = ['stream', 'timestamp', 'data']

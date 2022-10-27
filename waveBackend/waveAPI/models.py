from django.db import models
# Create your models here.


class Ship(models.Model):
    name = models.CharField(max_length=256, null=True)
    identifier = models.CharField(max_length=256, unique=True)


class MqttStream(models.Model):
    ship = models.ForeignKey(Ship, on_delete=models.CASCADE)
    mqtt_path = models.CharField(max_length=256)


class Entry(models.Model):
    stream = models.ForeignKey(MqttStream, on_delete=models.CASCADE)
    timestamp = models.FloatField()
    data = models.CharField(max_length=512)

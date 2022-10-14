from django.db import models
# Create your models here.


class MqttStream(models.Model):
    mqtt_path = models.CharField(max_length=255)


class Entry(models.Model):
    stream = models.ForeignKey(MqttStream, on_delete=models.CASCADE)
    data = models.JSONField()

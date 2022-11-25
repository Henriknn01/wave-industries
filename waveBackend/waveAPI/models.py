from django.db import models
# Create your models here.


class Ship(models.Model):
    """
    Ship database model
    """
    name = models.CharField(max_length=256, null=True)
    identifier = models.CharField(max_length=256, unique=True)

    def __str__(self):
        return self.name


class MqttStream(models.Model):
    """
    MqttStream database model
    """
    ship = models.ForeignKey(Ship, on_delete=models.CASCADE)
    mqtt_path = models.CharField(max_length=256, unique=True)

    def __str__(self):
        return self.mqtt_path


class Entry(models.Model):
    """
    Entry database model
    """
    stream = models.ForeignKey(MqttStream, on_delete=models.CASCADE)
    timestamp = models.DateTimeField()
    data = models.CharField(max_length=512)

    def __str__(self):
        return f"{self.stream} - {self.data}"

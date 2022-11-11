from django.contrib import admin

from waveAPI.models import Ship, MqttStream, Entry

# Register your models here.

admin.site.register(Ship)
admin.site.register(MqttStream)
admin.site.register(Entry)

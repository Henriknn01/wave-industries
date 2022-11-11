from .models import Ship, MqttStream, Entry
from django.shortcuts import render
from rest_framework import viewsets
from rest_framework import permissions
from .serializers import ShipSerializer, MqttStreamSerializer, EntrySerializer


# Create your views here.

class ShipViewSet(viewsets.ModelViewSet):
    queryset = Ship.objects.all()
    serializer_class = ShipSerializer
    permission_classes = [permissions.AllowAny]


class MqttStreamViewSet(viewsets.ModelViewSet):
    queryset = MqttStream.objects.all()
    serializer_class = MqttStreamSerializer
    permission_classes = [permissions.AllowAny]


class EntryViewSet(viewsets.ModelViewSet):
    queryset = Entry.objects.all()
    serializer_class = EntrySerializer
    permission_classes = [permissions.AllowAny]

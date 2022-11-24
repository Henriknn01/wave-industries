from datetime import datetime, timedelta

from .models import Ship, MqttStream, Entry
from django.shortcuts import render
from rest_framework import viewsets, generics
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


class EntryStreamView(generics.ListAPIView):
    serializer_class = EntrySerializer

    def get_queryset(self):
        """
        This view lets you filter data by stream and date, the default date interval is the last 24 hours

        :return: stream data within date interval
        """
        stream = self.request.query_params.get('stream')
        date_to = self.request.query_params.get('date-to', (datetime.now() + timedelta(hours=1)).isoformat()) # adds one hour to fix bug
        date_from = self.request.query_params.get('date-from', (datetime.now() - timedelta(days=1)).isoformat())
        return Entry.objects.filter(
            stream__mqtt_path=stream,
            timestamp__gte=date_from,
            timestamp__lte=date_to,
        )


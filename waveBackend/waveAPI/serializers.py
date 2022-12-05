from datetime import datetime, timedelta
from .models import Ship, MqttStream, Entry
from rest_framework import serializers


class ShipSerializer(serializers.HyperlinkedModelSerializer):
    """
    Serializes ship objects
    """
    class Meta:
        model = Ship
        fields = ['id', 'name', 'identifier', 'picture_url']


class MqttStreamSerializer(serializers.HyperlinkedModelSerializer):
    """
    Serializes mqtt stream objects
    """
    class Meta:
        model = MqttStream
        fields = ['id', 'ship', 'mqtt_path']


class EntrySerializer(serializers.ModelSerializer):
    """
    Serializes entry objects
    """
    stream = serializers.SlugRelatedField(
        queryset=MqttStream.objects.all(),
        slug_field='mqtt_path'
    )

    class Meta:
        model = Entry
        fields = ['id', 'stream', 'timestamp', 'data']


class ShipSummarySerializer(serializers.BaseSerializer):
    def to_representation(self, instance):
        # get data from the last 24 hours
        date_to = (datetime.now() + timedelta(hours=1)).isoformat()
        date_from = (datetime.now() - timedelta(days=1)).isoformat()

        co2_const = 0.00691  # change to realistic number
        nox_const = 0.00336  # change to realistic number
        nox_price = 23.79  # https://www.skatteetaten.no/satser/saravgift---nox/
        co2_price = 25  # https://www.regjeringen.no/no/tema/okonomi-og-budsjett/skatter-og-avgifter/avgiftssatser-2022/id2873933/
        taget_l_per_nm = 12

        try:
            total_fuel_consumption = Entry.objects.filter(
                stream__ship=instance,
                stream__mqtt_path=instance.mqttstream_set.get(mqtt_path=f'/{instance.identifier}/total_fuel_consumption'),
                timestamp__gte=date_from,
                timestamp__lte=date_to,
            )

            distance_sailed = Entry.objects.filter(
                stream__ship=instance,
                stream__mqtt_path=instance.mqttstream_set.get(mqtt_path=f'/{instance.identifier}/speed'),
                timestamp__gte=date_from,
                timestamp__lte=date_to,
            )

            fuel_level = Entry.objects.filter(
                stream__ship=instance,
                stream__mqtt_path=instance.mqttstream_set.get(mqtt_path=f'/{instance.identifier}/fuel_level'),
                timestamp__gte=date_from,
                timestamp__lte=date_to,
            )
            fuel_capacity = Entry.objects.filter(
                stream__ship=instance,
                stream__mqtt_path=instance.mqttstream_set.get(mqtt_path=f'/{instance.identifier}/fuel_capacity'),
                timestamp__gte=date_from,
                timestamp__lte=date_to,
            )

            energy_output = Entry.objects.filter(
                stream__ship=instance,
                stream__mqtt_path=instance.mqttstream_set.get(mqtt_path=f'/{instance.identifier}/engine/engine_output'),
                timestamp__gte=date_from,
                timestamp__lte=date_to,
            )

            energy_output_g1 = Entry.objects.filter(
                stream__ship=instance,
                stream__mqtt_path=instance.mqttstream_set.get(mqtt_path=f'/{instance.identifier}/generators/generator_1/engine_output'),
                timestamp__gte=date_from,
                timestamp__lte=date_to,
            )
            energy_output_g2 = Entry.objects.filter(
                stream__ship=instance,
                stream__mqtt_path=instance.mqttstream_set.get(mqtt_path=f'/{instance.identifier}/generators/generator_2/engine_output'),
                timestamp__gte=date_from,
                timestamp__lte=date_to,
            )

            heading = Entry.objects.filter(
                stream__ship=instance,
                stream__mqtt_path=instance.mqttstream_set.get(mqtt_path=f'/{instance.identifier}/heading'),
                timestamp__gte=date_from,
                timestamp__lte=date_to,
            ).latest('timestamp')

            distance_sum = 0
            fuel_sum = 0
            energy_sum = 0

            distance_list = list(distance_sailed)
            fuel_list = list(total_fuel_consumption)
            energy_list_main_engine = list(energy_output)
            energy_list_g1 = list(energy_output_g1)
            energy_list_g2 = list(energy_output_g2)

            for curr_entry, next_entry in zip(distance_list[:-1], distance_list[1:]):
                distance_sum += float(curr_entry.data) * (
                            ((next_entry.timestamp - curr_entry.timestamp).total_seconds() / 60) / 60)

            for curr_entry, next_entry in zip(fuel_list[:-1], fuel_list[1:]):
                fuel_sum += float(curr_entry.data) * (
                            ((next_entry.timestamp - curr_entry.timestamp).total_seconds() / 60) / 60)

            for curr_entry, next_entry in zip(energy_list_main_engine[:-1], energy_list_main_engine[1:]):
                energy_sum += float(curr_entry.data) * (
                            ((next_entry.timestamp - curr_entry.timestamp).total_seconds() / 60) / 60)

            for curr_entry, next_entry in zip(energy_list_g1[:-1], energy_list_g1[1:]):
                energy_sum += float(curr_entry.data) * (
                            ((next_entry.timestamp - curr_entry.timestamp).total_seconds() / 60) / 60)

            for curr_entry, next_entry in zip(energy_list_g2[:-1], energy_list_g2[1:]):
                energy_sum += float(curr_entry.data) * (
                            ((next_entry.timestamp - curr_entry.timestamp).total_seconds() / 60) / 60)

            fuel_consumed_per_nm = (fuel_sum / distance_sum) if distance_sum > 0 else 0
            fuel_level = (float(fuel_level.latest('timestamp').data) / float(
                fuel_capacity.latest('timestamp').data)) * 100

            nox_emissions = fuel_sum * nox_const
            nox_emissions_cost = nox_emissions * nox_price
            co2_emissions = fuel_sum * co2_const
            co2_emissions_cost = co2_emissions * co2_price
            fuel_efficiency = abs(fuel_consumed_per_nm / taget_l_per_nm)*100
            speed = float(distance_sailed.latest('timestamp').data)

            data = {
                'id': instance.id,
                'name': instance.name,
                'identifier': instance.identifier,
                'nm_sailed': round(distance_sum, 2),
                'fuel_consumed': round(fuel_sum, 2),
                'fuel_consumed_per_nm': round(fuel_consumed_per_nm, 2),
                'fuel_level': round(fuel_level, 2),
                'energy_produced': round(energy_sum, 2),
                'nox_emissions': round(nox_emissions, 2),
                'nox_cost': round(nox_emissions_cost, 2),
                'co2_emissions': round(co2_emissions, 2),
                'co2_cost': round(co2_emissions_cost, 2),
                'fuel_efficiency': round(fuel_efficiency, 2),
                'heading': round(float(heading.data), 2),
                'speed': round(speed, 2)
            }

            return data

        except Entry.DoesNotExist:
            data = {
                'id': instance.id,
                'name': instance.name,
                'identifier': instance.identifier,
                'nm_sailed': 0,
                'fuel_consumed': 0,
                'fuel_consumed_per_nm': 0,
                'fuel_level': 0,
                'energy_produced': 0,
                'nox_emissions': 0,
                'nox_cost': 0,
                'co2_emissions': 0,
                'co2_cost': 0,
                'fuel_efficiency': 0,
                'heading': 0,
                'speed': 0
            }
            return data

from rest_framework import serializers
from ..models.eventModel import Event


class EventSerializer(serializers.ModelSerializer):
    class Meta:
        model = Event
        fields = ["id", "name", "description", "start", "end"]

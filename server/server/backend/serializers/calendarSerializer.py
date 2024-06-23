from rest_framework import serializers
from ..models.calendarModel import Calendar
from ..serializers.eventSerializer import EventSerializer
from ..serializers.userSerializer import UserSerializer


class calendarSerializer(serializers.ModelSerializer):
    events = EventSerializer(many=True, read_only=False)

    class Meta:
        model = Calendar
        fields = ["id", "name", "description", "events"]

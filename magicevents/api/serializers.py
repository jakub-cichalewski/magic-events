from rest_framework import serializers
from rootapp.models import Event, EventRegistration


class EventSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Event
        fields = ['title', 'start_date', 'end_date', 'thumbnail']

from rest_framework import serializers
from rootapp.models import Event, EventRegistration


class EventSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Event
        fields = ['title', 'start_date', 'end_date', 'thumbnail']


class EventRegistrationSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = EventRegistration
        fields = ['event', 'registration_code']
    # TODO: add a field to display event.title

from django.shortcuts import render
from rest_framework import viewsets

from api.serializers import EventSerializer, EventRegistrationSerializer
from rootapp.models import Event, EventRegistration


class EventViewSet(viewsets.ModelViewSet):
    queryset = Event.objects.all().order_by('start_date')
    serializer_class = EventSerializer
    http_method_names = ['get']


class EventRegistrationViewSet(viewsets.ModelViewSet):
    queryset = EventRegistration.objects.all()
    serializer_class = EventRegistrationSerializer
    http_method_names = ['get']
    

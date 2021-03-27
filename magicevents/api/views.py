from django.shortcuts import render
from rest_framework import viewsets

from api.serializers import EventSerializer
from rootapp.models import Event


class EventViewSet(viewsets.ModelViewSet):
    queryset = Event.objects.all().order_by('start_date')
    serializer_class = EventSerializer
    http_method_names = ['get', 'head']

from django.urls import path, include
from django.conf.urls import url

from rootapp.views import start, register, events, register_for_event, unregister_from_event

urlpatterns = [
    path('register/', register, name='register'),
    path('events/', events, name='events'),
    path('events/register/', register_for_event, name='register_for_event'),
    path('events/unregister/', unregister_from_event, name='unregister_from_event'),
    path('', start, name='start'),
    path('accounts/', include('django.contrib.auth.urls')),
]

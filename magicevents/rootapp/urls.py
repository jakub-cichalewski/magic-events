from django.urls import path, include
# from django.conf.urls import url

from rootapp.views import start, register,\
 events, event_register, event_unregister

urlpatterns = [
    path('register/', register, name='register'),
    path('events/', events, name='events'),
    path('events/register/', event_register, name='register_for_event'),
    path('events/unregister/', event_unregister, name='unregister_from_event'),
    path('', start, name='start'),
    path('accounts/', include('django.contrib.auth.urls')),
]

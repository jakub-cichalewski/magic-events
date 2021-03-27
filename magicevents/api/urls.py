from django.urls import include, path
from rest_framework import routers

from api.views import EventViewSet
from api.views import EventRegistrationViewSet

router = routers.DefaultRouter()
router.register('events', EventViewSet)
router.register('event-registrations', EventRegistrationViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('api-auth/', include('rest_framework.urls',
        namespace='rest_framework')),
]

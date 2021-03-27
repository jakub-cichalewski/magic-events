from django.urls import include, path
from rest_framework import routers

from api.views import EventViewSet

router = routers.DefaultRouter()
router.register('events', EventViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('api-auth/', include('rest_framework.urls',
        namespace='rest_framework')),
]

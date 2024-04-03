from django.urls import path, include
from rest_framework import routers

from service.views import SubscriptionViewSet

router = routers.DefaultRouter()
router.register(r'api/v1/subscriptions', SubscriptionViewSet, basename='subscriptions')
urlpatterns = [
    path('', include(router.urls)),
]
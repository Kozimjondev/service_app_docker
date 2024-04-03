from django.shortcuts import render
from rest_framework import viewsets

from service.models import Subscription
from service.serializers import SubscriptionSerializer


# Create your views here.
class SubscriptionViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Subscription.objects.all()
    serializer_class = SubscriptionSerializer

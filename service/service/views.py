from django.db.models import Prefetch
from rest_framework import viewsets

from client.models import Client
from service.models import Subscription
from service.serializers import SubscriptionSerializer


# Create your views here.
class SubscriptionViewSet(viewsets.ReadOnlyModelViewSet):
    # queryset = Subscription.objects.all().prefetch_related('client').select_related('client__user')
    queryset = Subscription.objects.all().select_related('service', 'plan').prefetch_related(
        Prefetch('client', queryset=Client.objects.select_related('user').only('company',
                                                                               'user__email',
                                                                               'user__username'))
    )
    serializer_class = SubscriptionSerializer

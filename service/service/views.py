from django.core.cache import cache

from django.db.models import Prefetch, F, Sum
from rest_framework import viewsets, status
from rest_framework.response import Response

from client.models import Client
from django.conf import settings
from service.models import Subscription
from service.serializers import SubscriptionSerializer


# Create your views here.
class SubscriptionViewSet(viewsets.ReadOnlyModelViewSet):
    # queryset = Subscription.objects.all().prefetch_related('client').select_related('client__user')
    queryset = Subscription.objects.all().select_related('service', 'plan').prefetch_related(
        Prefetch('client', queryset=Client.objects.select_related('user').only('company',
                                                                               'user__email',
                                                                               'user__username'))
    )  # .annotate(price=F('service__full_price') - F('service__full_price') * F('plan__discount') / 100.00)
    serializer_class = SubscriptionSerializer

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())

        response = super(SubscriptionViewSet, self).list(request, *args, **kwargs)

        price_cache = cache.get(settings.PRICE_CACHE_NAME)

        if price_cache:
            total_price = price_cache
        else:
            total_price = queryset.aggregate(total=Sum('price')).get('total', 0)
            cache.set(settings.PRICE_CACHE_NAME, total_price, 60*60)

        response_data = {'result': response.data,
                         'total_amount': total_price}

        return Response(response_data, status=status.HTTP_200_OK)

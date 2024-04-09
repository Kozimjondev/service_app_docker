from datetime import time

from celery import shared_task
from django.conf import settings
from django.core.cache import cache
# from celery_singleton import Singleton
from django.db.models import F


@shared_task()
def set_price(subscription_id):
    from service.models import Subscription

    # subscription = Subscription.objects.get(id=subscription_id)

    subscription = Subscription.objects.filter(id=subscription_id
                                               ).annotate(annotated_price=F('service__full_price') -
                                                                F('service__full_price') *
                                                                F('plan__discount') / 100.00).first()
    # new_price = (subscription.service.full_price -
    #              subscription.service.full_price * subscription.plan.discount / 100.00)

    subscription.price = subscription.annotated_price
    # subscription.price = new_price

    subscription.save()

    cache.delete(settings.PRICE_CACHE_NAME)
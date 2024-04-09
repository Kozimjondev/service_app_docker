from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models
from django.db.models.signals import post_delete
from django.utils.translation import ugettext_lazy as _

from client.models import Client
from service.signals import delete_cache_total_sum
from service.tasks import set_price


# Create your models here.
class Service(models.Model):
    name = models.CharField(max_length=100)
    full_price = models.PositiveIntegerField()

    def __str__(self):
        return f"{self.name} - {self.full_price}"

    def __init__(self, *args, **kwargs):
        super(Service, self).__init__(*args, **kwargs)
        self.__full_price = self.full_price

    def save(self, *args, **kwargs):
        if self.full_price != self.__full_price:
            for subscription in self.subscriptions.all():
                set_price.delay(subscription.id)
        return super(Service, self).save(*args, **kwargs)


class Plan(models.Model):
    PLAN_CHOICES = (
        ('full', 'Full'),
        ('student', 'Student'),
        ('discount', 'Discount'),
    )
    plan_type = models.CharField(_("Plan type"),
                                 max_length=20,
                                 choices=PLAN_CHOICES)
    discount = models.PositiveIntegerField(_("Discount"), default=0,
                                           validators=[MinValueValidator(0),
                                                       MaxValueValidator(100)])

    def __init__(self, *args, **kwargs):
        super(Plan, self).__init__(*args, **kwargs)
        self.__discount = self.discount

    def save(self, *args, **kwargs):
        if self.discount != self.__discount:
            for subscription in self.subscriptions.all():
                set_price.delay(subscription.id)
        return super(Plan, self).save(*args, **kwargs)

    def __str__(self):
        return f"{self.plan_type} - {self.discount}%"

    class Meta:
        unique_together = ('plan_type',)


class Subscription(models.Model):
    client = models.ForeignKey(Client,
                               on_delete=models.CASCADE,
                               related_name='subscriptions')
    service = models.ForeignKey(Service,
                                on_delete=models.CASCADE,
                                related_name='subscriptions')
    plan = models.ForeignKey(Plan,
                             on_delete=models.CASCADE,
                             related_name='subscriptions')
    price = models.PositiveIntegerField(_("Price"), default=0)

    def __str__(self):
        return f"{self.client.user.username} - {self.service.name} - {self.plan.plan_type}"

    def save(self, *args, save_model=True, **kwargs):
        creating = not bool(self.pk)
        result = super(Subscription, self).save(*args, **kwargs)
        if creating:
            set_price.delay(self.pk)
        return result

    class Meta:
        unique_together = ('client', 'service')


post_delete.connect(delete_cache_total_sum, sender=Subscription)

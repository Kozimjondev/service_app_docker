from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models
from django.utils.translation import ugettext_lazy as _

from client.models import Client


# Create your models here.
class Service(models.Model):
    name = models.CharField(max_length=100)
    full_price = models.PositiveIntegerField()

    def __str__(self):
        return f"{self.name} - {self.full_price}"


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

    def __str__(self):
        return f"{self.client.user.username} - {self.service.name} - {self.plan.plan_type}"

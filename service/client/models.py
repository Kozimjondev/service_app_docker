from django.contrib.auth.models import User
from django.db import models
from django.utils.translation import ugettext_lazy as _


# Create your models here.
class Client(models.Model):
    user = models.OneToOneField(User, on_delete=models.PROTECT)
    company = models.CharField(_("Company name"), max_length=100)
    full_address = models.CharField(_("Full address"), max_length=100)

    def __str__(self):
        return self.user.username

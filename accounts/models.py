from django.db import models
from django.conf import settings
from django.contrib.auth.models import User


class Subscription(models.Model):
    BOOL_CHOICES = (
        (True, 'Yes'),
        (False, 'No'),
    )
    accountuser = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
    )
    ordernumber = models.IntegerField(blank = False, null=False)
    substart = models.DateTimeField(null=False, blank=False)
    subend = models.DateTimeField(null=False, blank=False)
    active = models.BooleanField(choices = BOOL_CHOICES)
    isrunning = models.BooleanField()

    class Meta:
        managed=True
        db_table = 'Subscription'
        verbose_name_plural = 'Subscriptions'

   
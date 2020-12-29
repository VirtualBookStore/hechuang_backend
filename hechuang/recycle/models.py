from django.db import models

from notifications.models import Notification
from order.models import Order


class RecycleRequest(models.Model):
    order = models.OneToOneField(Order, on_delete=models.CASCADE, primary_key=True)
    message = models.TextField(blank=True)
    price = models.IntegerField(default=0)
    allowed = models.BooleanField(null=True)
    read = models.BooleanField(default=False)
    number = models.IntegerField(default=1)
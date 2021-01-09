from django.db import models

from notifications.models import Notification
from order.models import Order


class RecycleRequest(models.Model):
    order = models.OneToOneField(Order, on_delete=models.CASCADE, primary_key=True)

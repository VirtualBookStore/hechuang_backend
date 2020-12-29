from django.db import models
from django.contrib.auth.models import User, AbstractUser
# Create your models here.


class HechuangUser(AbstractUser):
    address = models.TextField(blank=True)

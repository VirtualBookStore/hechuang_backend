from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver


class Book(models.Model):
    isbn = models.CharField(max_length=10, primary_key=True, null=False, unique=True)
    title = models.CharField(max_length=50)
    description = models.TextField(blank=True)
    tag = models.CharField(max_length=50, blank=True)
    price = models.IntegerField(blank=True)
    new_total = models.IntegerField(default=0)
    old_total = models.IntegerField(default=0)
    recommended = models.BooleanField(default=False)
    cover = models.ImageField(upload_to='', null=True)

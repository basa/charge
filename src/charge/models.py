# -*- coding: utf-8 -*-

from django.contrib.auth.models import User
from django.db import models
from djmoney.models.fields import MoneyField


class Event(models.Model):
    creator = models.ForeignKey(User, related_name='+')
    participants = models.ManyToManyField(User)
    name = models.CharField(max_length=255)
    location = models.CharField(max_length=255)
    start_date = models.DateTimeField()


class Item(models.Model):
    creator = models.ForeignKey(User)
    event = models.ForeignKey(Event)
    name = models.CharField(max_length=255)
    cost = MoneyField(max_digits=12, decimal_places=2, default_currency='EUR')
    receipt = models.FileField(upload_to='receipts/%Y/%m/%d')
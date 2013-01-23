# -*- coding: utf-8 -*-

from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.db import models
from djmoney.models.fields import MoneyField


class Event(models.Model):
    """
    Event with participants.
    """
    creator = models.ForeignKey(User, related_name='+')
    participants = models.ManyToManyField(User)
    name = models.CharField(max_length=255)
    location = models.CharField(max_length=255)
    start_date = models.DateTimeField()

    def get_absolute_url(self):
        return reverse('event', args=[str(self.pk)])


class Item(models.Model):
    """
    Cost can be positive and negative.
    """
    creator = models.ForeignKey(User)
    event = models.ForeignKey(Event)
    name = models.CharField(max_length=255)
    cost = MoneyField(max_digits=12, decimal_places=2, default_currency='EUR')
    receipt = models.FileField(upload_to='receipts/%Y/%m/%d', null=True,
            blank=True)

    def get_absolute_url(self):
        return reverse('item', args=[str(self.pk)])


class Bill(models.Model):
    pass

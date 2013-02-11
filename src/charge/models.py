# -*- coding: utf-8 -*-
import datetime

from django.contrib.auth.models import User
from django.contrib.admin.models import LogEntry
from django.core.urlresolvers import reverse
from django.db import models
from django.utils.translation import ugettext_lazy as __
from djmoney.models.fields import MoneyField


class EventLogEntry(LogEntry):
    class Meta:
        db_table = 'event_log'


class Event(models.Model):
    """
    Event with participants.
    """
    creator = models.ForeignKey(User, related_name='+')
    participants = models.ManyToManyField(User)
    name = models.CharField(max_length=255)
    location = models.CharField(max_length=255)
    start_date = models.DateTimeField(default=datetime.datetime.now)

    class Meta:
        verbose_name = __('Event')

    def get_absolute_url(self):
        return reverse('event', args=[str(self.pk)])

    def __unicode__(self):
        return self.name


class Item(models.Model):
    """
    Attributes:
        cost: can be positive and negative.
    """
    creator = models.ForeignKey(User)
    event = models.ForeignKey(Event)
    name = models.CharField(max_length=255)
    cost = MoneyField(max_digits=12, decimal_places=2, default_currency='EUR')
    receipt = models.FileField(upload_to='receipts/%Y/%m/%d', null=True,
            blank=True)

    class Meta:
        verbose_name = __('Item')

    def __unicode__(self):
        return self.name

# -*- coding: utf-8 -*-
import datetime

from django.contrib.auth.models import User
from django.contrib.admin.models import LogEntry
from django.core.urlresolvers import reverse
from django.db import models
from django.utils.translation import ugettext_lazy as __
from djmoney.models.fields import MoneyField
from moneyed.classes import Money


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

    def find_or_create_payment_with_user(self, user):
        payments = self.payment_set.filter(user=user)
        if payments.count() < 1:
            payment = Payment(user=user)
            self.payment_set.add(payment)
            return payment
        else:
            return payments[0]

    def bill(self):
        from charge.utils import convert
        currency = 'EUR'
        # accumulate items
        event_cost = Money(amount='0.00', currency=currency)
        paid = {}
        for user in self.participants.all():
            paid[user] = Money(amount='0.00', currency=currency)
        currency_cache = {}
        for item in self.item_set.all():
            item_cost = convert(
              item.cost,
              currency,
              currency_cache
            )
            event_cost += item_cost
            paid[item.creator] += item_cost
        balance = event_cost / self.participants.count()
        for user in self.participants.all():
            imbalance = paid[user] - balance
            payment = self.find_or_create_payment_with_user(user)
            payment.amount = imbalance
            payment.is_paid = False
            payment.save()

    def unbill(self):
        self.payment_set.all().delete()

    def is_billed(self):
        return self.payment_set.all().count() > 0

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


class Payment(models.Model):
    user = models.ForeignKey(User)
    event = models.ForeignKey(Event)
    amount = MoneyField(max_digits=12, decimal_places=2, default_currency='EUR')
    is_paid = models.BooleanField()

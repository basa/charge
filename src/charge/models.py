# -*- coding: utf-8 -*-
import datetime

from django.contrib.auth.models import User
from django.contrib.admin.models import LogEntry
from django.core.urlresolvers import reverse
from django.db import models
from django.utils.translation import ugettext_lazy as __
from django.db.models import Sum
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
        currency = 'EUR'
        # accumulate items
        event_cost = Money(amount='0.00', currency=currency)
        participants = self.participants.all()
        paid = {}

        for user in participants:
            paid[user] = Money(amount='0.00', currency=currency)
        for item in self.item_set.all():
            item_cost = item.convert_cost(currency)
            event_cost += item_cost
            paid[item.creator] += item_cost
        balance = event_cost / len(participants)
        for user in participants:
            imbalance = paid[user] - balance
            payment = self.find_or_create_payment_with_user(user)
            payment.amount = imbalance
            payment.is_paid = False
            if user == self.creator:
                payment.is_paid = True
            payment.save()

    def unbill(self):
        self.payment_set.all().delete()

    def is_billed(self):
        return self.payment_set.all().count() > 0

    def is_done(self):
        return (self.is_billed() and
                not self.payment_set.filter(is_paid=False).exists())

    def user_open_inbound_payments(self, user):
        if user == self.creator:
            result = self.payment_set.filter(is_paid=False, amount__lt=0).aggregate(Sum('amount'))['amount__sum']
            return -result if result else result
        return self.payment_set.filter(user=user, is_paid=False, amount__gt=0).aggregate(Sum('amount'))['amount__sum']

    def user_open_outbound_payments(self, user):
        if user == self.creator:
            return self.payment_set.filter(is_paid=False, amount__gt=0).aggregate(Sum('amount'))['amount__sum']
        result = self.payment_set.filter(user=user, is_paid=False, amount__lt=0).aggregate(Sum('amount'))['amount__sum']
        return -result if result else result


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

    def convert_cost(self, to_currency='EUR'):
        from charge.utils import convert
        return convert(self.cost, to_currency)


class Payment(models.Model):
    user = models.ForeignKey(User)
    event = models.ForeignKey(Event)
    amount = MoneyField(max_digits=12, decimal_places=2, default_currency='EUR')
    is_paid = models.BooleanField()

    class Meta:
        unique_together = ('user', 'event')

    def receiver(self):
        if self.user == self.event.creator:
            return None
        elif self.amount.amount > 0:
            return self.user
        elif self.amount.amount < 0:
            return self.event.creator
        else:
            return None

# -*- coding: utf-8 -*-

from django import forms

from bootstrap.forms import BootstrapMixin

from charge.models import Event, Item


class EventForm(BootstrapMixin, forms.ModelForm):

    class Meta:
        model = Event


class ItemForm(BootstrapMixin, forms.ModelForm):

    class Meta:
        model = Item

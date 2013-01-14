# -*- coding: utf-8 -*-

from django import forms

from bootstrap.forms import BootstrapMixin
from registration.forms import RegistrationFormUniqueEmail

from charge.models import Event, Item


class RegistrationForm(BootstrapMixin, RegistrationFormUniqueEmail):
    pass


class EventForm(BootstrapMixin, forms.ModelForm):

    class Meta:
        model = Event


class ItemForm(BootstrapMixin, forms.ModelForm):

    class Meta:
        model = Item

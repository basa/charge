# -*- coding: utf-8 -*-

from django import forms

from bootstrap.forms import BootstrapMixin, Fieldset
from registration.forms import RegistrationFormUniqueEmail

from charge.models import Event, Item


class RegistrationForm(BootstrapMixin, RegistrationFormUniqueEmail):
    pass


class EventForm(BootstrapMixin, forms.ModelForm):

    class Meta:
        model = Event
        # creator would be assigned programmatically
        exclude = ('creator',)
        layout = (
            Fieldset('Add a Event', 'name', 'location', 'start_date',
                    'participants'),
        )


class ItemForm(BootstrapMixin, forms.ModelForm):

    class Meta:
        model = Item

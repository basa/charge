# -*- coding: utf-8 -*-

from bootstrap.forms import BootstrapMixin, BootstrapModelForm, Fieldset
from registration.forms import RegistrationFormUniqueEmail

from charge.models import Event, Item


class RegistrationForm(BootstrapMixin, RegistrationFormUniqueEmail):
    """
    BootstrapForm for registration with unique email.
    """

    pass


class EventForm(BootstrapModelForm):
    """
    BootstrapForm for Event model.
    """

    class Meta:
        model = Event
        # creator would be assigned programmatically
        exclude = ('creator',)
        layout = (
            Fieldset('Add a Event', 'name', 'location', 'start_date',
                    'participants'),
        )


class ItemForm(BootstrapModelForm):
    """
    BootstrapForm for Item model.
    """

    class Meta:
        model = Item
        # creator would be assigned programmatically
        exclude = ('creator',)
        layout = (
            Fieldset('Add a Item', 'event', 'name', 'cost',
                    'receipt'),
        )

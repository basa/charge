# -*- coding: utf-8 -*-
from bootstrap.forms import BootstrapMixin, BootstrapModelForm, Fieldset
from django.contrib.auth import forms as auth_forms
from django.forms.widgets import SplitDateTimeWidget
from registration.forms import RegistrationFormUniqueEmail

from charge.models import Event, Item


class BaseForm(BootstrapModelForm):
    def __init__(self, *args, **kwargs):
        """ Generate legend text automatically. """
        super(BaseForm, self).__init__(*args, **kwargs)

        status = 'Create' if self.instance._state.adding else 'Update'
        model_name = self.Meta.model._meta.verbose_name
        self.Meta.layout[0].legend = '{status} {model_name}'.format(
                model_name=model_name, status=status)


class EventForm(BaseForm):
    """
    BootstrapForm for Event model.
    """
    class Meta:
        model = Event
        # creator would be assigned programmatically
        exclude = ('creator',)
        layout = (
            Fieldset('', 'name', 'location', 'start_date',
                    'participants'),
        )
        widgets = {
            'start_date': SplitDateTimeWidget(attrs={'class': 'datepicker'}),
        }


class ItemForm(BaseForm):
    """
    BootstrapForm for Item model.
    """
    class Meta:
        model = Item
        # creator would be assigned programmatically
        exclude = ('creator',)
        layout = (
            Fieldset('', 'event', 'name', 'cost',
                    'receipt'),
        )
        enctype = 'multipart/form-data'


class AuthenticationForm(BootstrapMixin, auth_forms.AuthenticationForm):
    """
    BootstrapForm for authentication.
    """
    pass


class RegistrationForm(BootstrapMixin, RegistrationFormUniqueEmail):
    """
    BootstrapForm for registration with unique email.
    """
    pass

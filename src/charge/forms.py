# -*- coding: utf-8 -*-
from bootstrap.forms import BootstrapMixin, BootstrapModelForm, Fieldset
from django.contrib.auth import forms as auth_forms
from django.contrib.auth import models as auth_models
from django.forms.widgets import SplitDateTimeWidget
from django.utils.translation import ugettext_lazy as __
from registration.forms import RegistrationFormUniqueEmail

from charge.models import Event, Item


class BaseForm(BootstrapModelForm):
    def __init__(self, *args, **kwargs):
        """ Generate legend text automatically. """
        super(BaseForm, self).__init__(*args, **kwargs)
        legend = (__('Create {model_name}') if self.instance._state.adding
                else __('Update {model_name}'))
        model_name = self.Meta.model._meta.verbose_name
        self.Meta.layout[0].legend = legend.format(model_name=model_name)


class EventForm(BaseForm):
    """
    BootstrapForm for Event model.
    """
    class Meta:
        model = Event
        # creator would be assigned programmatically
        exclude = ('creator',)
        layout = (
            Fieldset('', 'name', 'location', 'start_date', 'participants'),
        )
        widgets = {
            'start_date': SplitDateTimeWidget(attrs={'class': 'datepicker'}),
        }

    def __init__(self, *args, **kwargs):
        super(EventForm, self).__init__(**kwargs)
        # staff users can not be participants
        self.fields['participants'].queryset = (
                auth_models.User.objects.exclude(is_staff=True))


class ItemForm(BaseForm):
    """
    BootstrapForm for Item model.
    """
    class Meta:
        model = Item
        # creator and event would be assigned programmatically
        exclude = ('creator', 'event')
        layout = (
            Fieldset('', 'name', 'cost', 'receipt'),
        )


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

# -*- coding: utf-8 -*-

from django import forms

from charge.models import Event, Item


class EventForm(forms.ModelForm):

    class Meta:
        model = Event


class ItemForm(forms.ModelForm):

    class Meta:
        model = Item

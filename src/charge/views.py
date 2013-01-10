# -*- coding: utf-8 -*-

from django.views.generic import edit

from charge.models import Event, Item


class EventCreate(edit.CreateView):
    model = Event


class EventUpdate(edit.UpdateView):
    model = Event


class EventDelete(edit.DeleteView):
    model = Event


class ItemCreate(edit.CreateView):
    model = Item


class ItemUpdate(edit.UpdateView):
    model = Item


class ItemDelete(edit.DeleteView):
    model = Item
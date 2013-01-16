# -*- coding: utf-8 -*-

from django.views.generic import edit
from django.core.urlresolvers import reverse_lazy

from charge import forms, models


class EventCreate(edit.CreateView):
    model = models.Event
    form_class = forms.EventForm
    success_url = reverse_lazy('events')

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.creator = self.request.user
        self.object.save()

        return super(EventCreate, self).form_valid(form)


class EventUpdate(edit.UpdateView):
    model = models.Event


class EventDelete(edit.DeleteView):
    model = models.Event


class ItemCreate(edit.CreateView):
    model = models.Item


class ItemUpdate(edit.UpdateView):
    model = models.Item


class ItemDelete(edit.DeleteView):
    model = models.Item
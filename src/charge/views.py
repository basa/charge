# -*- coding: utf-8 -*-

from django.views.generic import detail, edit, list
from django.core.urlresolvers import reverse_lazy

from charge import forms, models


class CreatorMixin(object):
    """
    Assigns requesting user as creator to the model object.
    """
    def form_valid(self, form):
        form.instance.creator = self.request.user
        return super(CreatorMixin, self).form_valid(form)


class BaseCreateView(CreatorMixin, edit.CreateView):
    pass


class BaseUpdateView(CreatorMixin, edit.UpdateView):
    """
    success_url_name
    """
    def get_success_url(self):
        return reverse_lazy(self.success_url_name, args=[self.object.pk])


class EventCreate(BaseCreateView):
    model = models.Event
    form_class = forms.EventForm
    success_url = reverse_lazy('overview')


class EventDetail(detail.DetailView):
    """
    Represents an individual Event object.
    """
    model = models.Event

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super(EventDetail, self).get_context_data(**kwargs)
        # Add in Items
        context['items'] = models.Item.objects.filter(event=self.object)

        return context


class EventUpdate(BaseUpdateView):
    model = models.Event
    form_class = forms.EventForm
    success_url_name = 'event'


# TODO add has delete permission decorator
class EventDelete(edit.DeleteView):
    model = models.Event


# TODO add event parameter
class ItemCreate(BaseCreateView):
    model = models.Item
    form_class = forms.ItemForm
    success_url = reverse_lazy('overview')


class ItemUpdate(BaseUpdateView):
    model = models.Item
    form_class = forms.ItemForm
    success_url_name = 'item'


# TODO add has delete permission decorator
class ItemDelete(edit.DeleteView):
    model = models.Item


class Overview(list.ListView):
    template_name = 'charge/overview.html'

    def get_queryset(self):
        current_user = self.request.user

        return models.Event.objects.filter(creator=current_user)

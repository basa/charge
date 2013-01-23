# -*- coding: utf-8 -*-

from django.core.urlresolvers import reverse_lazy
from django.db.models import Q
from django.views.generic import detail, edit, list

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
    Attributes:
        success_url_name
    """
    def get_success_url(self):
        return reverse_lazy(self.success_url_name, args=[self.object.pk])

    def get_queryset(self):
        """ User should only update his objects. """
        base_qs = super(BaseUpdateView, self).get_queryset()
        current_user = self.request.user
        return base_qs.filter(creator=current_user)


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
    model = models.Event
    template_name = 'charge/overview.html'

    def get_queryset(self):
        """ User should only see his objects. """
        base_qs = super(Overview, self).get_queryset()
        current_user = self.request.user
        return base_qs.filter(Q(creator=current_user) |
                Q(participants=current_user))

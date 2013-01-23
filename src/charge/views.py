# -*- coding: utf-8 -*-

from django.core.urlresolvers import reverse_lazy
from django.db.models import Q
from django.views.generic import detail, edit, list

from charge import forms, models
from charge.utils import login_required


### Mixins ####################################################################

class CreatorMixin(object):
    """
    Assigns requesting user as creator to the model object.
    """
    def form_valid(self, form):
        form.instance.creator = self.request.user
        return super(CreatorMixin, self).form_valid(form)


class FilterCreatorMixin(object):
    """
    User should only access his objects.
    """
    def get_queryset(self):
        """ Queryset is filtered creator == request.user. """
        base_qs = super(FilterCreatorMixin, self).get_queryset()
        current_user = self.request.user
        return base_qs.filter(creator=current_user)


### BaseViews #################################################################

class BaseCreateView(CreatorMixin, edit.CreateView):
    success_url = reverse_lazy('overview')


class BaseUpdateView(FilterCreatorMixin, edit.UpdateView):
    """
    Attributes:
        success_url_name
    """
    def get_success_url(self):
        return reverse_lazy(self.success_url_name, args=[self.object.pk])


class BaseDeleteView(FilterCreatorMixin, edit.DeleteView):
    """
    DeleteView with user filter and redirect to Overview.
    """
    success_url = reverse_lazy('overview')


### Event Related #############################################################

@login_required
class EventCreate(BaseCreateView):
    model = models.Event
    form_class = forms.EventForm


@login_required
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


@login_required
class EventUpdate(BaseUpdateView):
    model = models.Event
    form_class = forms.EventForm
    success_url_name = 'event'


@login_required
class EventDelete(BaseDeleteView):
    model = models.Event


### Item related ##############################################################

# TODO add event parameter
@login_required
class ItemCreate(BaseCreateView):
    model = models.Item
    form_class = forms.ItemForm


@login_required
class ItemUpdate(BaseUpdateView):
    model = models.Item
    form_class = forms.ItemForm
    success_url_name = 'item'


@login_required
class ItemDelete(BaseDeleteView):
    model = models.Item


@login_required
class Overview(list.ListView):
    model = models.Event
    template_name = 'charge/overview.html'

    def get_queryset(self):
        """ User should only see his objects. """
        base_qs = super(Overview, self).get_queryset()
        current_user = self.request.user
        return base_qs.filter(Q(creator=current_user) |
                Q(participants=current_user)).distinct()

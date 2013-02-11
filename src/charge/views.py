# -*- coding: utf-8 -*-

from django.http import Http404
from django.contrib import messages
from django.contrib.auth import views as auth_views
from django.core.urlresolvers import reverse, reverse_lazy
from django.db.models import Q, Sum
from django.utils.translation import ugettext as _
from django.utils.translation import ugettext_lazy as __
from django.views.generic import base, detail, edit, list
from django.shortcuts import get_object_or_404, redirect

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
    Limit a User to only obtain their own data.
    """
    def get_queryset(self):
        """ Limit the queryset to the requesting user. """
        base_qs = super(FilterCreatorMixin, self).get_queryset()
        current_user = self.request.user
        return base_qs.filter(creator=current_user)


### BaseViews #################################################################

class BaseCreateView(CreatorMixin, edit.CreateView):
    """
    The used Model should have a creator and name field.
    """
    success_message = __('{name} created successfully')

    def form_valid(self, form):
        """ Display success message. """
        name = form.cleaned_data['name']
        msg = self.success_message.format(name=name)
        messages.success(self.request, msg)
        return super(BaseCreateView, self).form_valid(form)


class BaseUpdateView(FilterCreatorMixin, edit.UpdateView):
    """
    The used Model should have a creator and name field.
    """
    success_message = __('{name} updated successfully')

    def form_valid(self, form):
        """ Display success message. """
        name = self.object.name
        msg = self.success_message.format(name=name)
        messages.success(self.request, msg)
        return super(BaseUpdateView, self).form_valid(form)


class BaseDeleteView(FilterCreatorMixin, edit.DeleteView):
    """
    DeleteView with user filter and redirect to Overview.

    The used Model should have a creator and name field.
    """
    success_message = __('{name} deleted successfully')
    template_name = 'charge/object_confirm_delete.html'

    def delete(self, request, *args, **kwargs):
        """ Display success message. """
        name = self.get_object().name
        msg = self.success_message.format(name=name)
        messages.success(self.request, msg)
        return super(BaseDeleteView, self).delete(request, *args, **kwargs)


class Index(base.TemplateView):
    template_name = 'index.html'

    def get_context_data(self, **kwargs):
        context = super(Index, self).get_context_data(**kwargs)
        # FIXME convert to base currency
        context['total_costs'] = models.Item.objects.aggregate(
                total_costs=Sum('cost'))['total_costs']
        return context


### Event Related #############################################################

@login_required
class EventCreate(BaseCreateView):
    model = models.Event
    form_class = forms.EventForm
    success_url = reverse_lazy('overview')

    def get_initial(self):
        initial = super(EventCreate, self).get_initial()
        # request user is default participant
        initial['participants'] = [self.request.user.pk]
        return initial


@login_required
class EventDetail(detail.DetailView):
    """
    Represents an individual Event object.
    """
    model = models.Event

    def get_context_data(self, **kwargs):
        context = super(EventDetail, self).get_context_data(**kwargs)
        context['items'] = models.Item.objects.filter(event=self.object)
        participants = self.object.participants.all();
        for participant in participants:
            payments = self.object.payment_set.filter(user=participant)
            if (payments.count() >= 1):
                participant.payment = payments[0]
        context['participants'] = participants
        return context


@login_required
class EventUpdate(BaseUpdateView):
    model = models.Event
    form_class = forms.EventForm

    def get_success_url(self):
        return reverse_lazy('event', args=[self.object.pk])


@login_required
class EventDelete(BaseDeleteView):
    model = models.Event
    success_url = reverse_lazy('overview')

def event_bill(request, pk):
    event = models.Event.objects.get(pk=pk)
    if not request.user == event.creator:
        raise Http404()
    event.bill()
    return redirect(event.get_absolute_url())

def event_unbill(request, pk):
    event = models.Event.objects.get(pk=pk)
    if not request.user == event.creator:
        raise Http404()
    event.unbill()
    return redirect(event.get_absolute_url())

### Item related ##############################################################

class ItemSuccessUrlMixin(object):
    """
    Redirects to corresponding event.
    """
    def get_success_url(self):
        return reverse_lazy('event', args=[self.object.event.pk])


@login_required
class ItemCreate(ItemSuccessUrlMixin, BaseCreateView):
    """
    Create Item for given Event.
    """
    model = models.Item
    form_class = forms.ItemForm

    def post(self, request, *args, **kwargs):
        # request user must participant in related Event
        self.event = get_object_or_404(models.Event,
                pk=self.kwargs['event_pk'], participants=self.request.user)
        return super(ItemCreate, self).post(self, request, *args, **kwargs)

    def form_valid(self, form):
        """ Assigns event to form. """
        form.instance.event = self.event
        return super(ItemCreate, self).form_valid(form)


@login_required
class ItemUpdate(ItemSuccessUrlMixin, BaseUpdateView):
    model = models.Item
    form_class = forms.ItemForm


@login_required
class ItemDelete(ItemSuccessUrlMixin, BaseDeleteView):
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


@login_required
class Logout(base.View):
    def get(self, request, *args, **kwargs):
        """
        Signs out the user and adds a success message.
        """
        messages.success(request, _('You have been signed out.'),
                fail_silently=True)
        login_url = reverse('auth_login')
        return auth_views.logout(request, next_page=login_url, *args, **kwargs)


def user(request, user):
    if user == request.user.username:
        return redirect('/overview/')
    else:
        raise Http404()

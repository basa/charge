# -*- coding: utf-8 -*-

from django.http import Http404
from django.contrib import messages
from django.contrib.admin.models import ADDITION, CHANGE, DELETION
from django.contrib.auth import views as auth_views
from django.contrib.contenttypes.models import ContentType
from django.core.urlresolvers import reverse, reverse_lazy
from django.db.models import Q, Sum
from django.http import HttpResponseRedirect
from django.utils.translation import ugettext as _
from django.utils.translation import ugettext_lazy as __
from django.views.generic import base, detail, edit, list
from django.shortcuts import get_object_or_404, redirect

from charge import forms, models
from charge.utils import create_log_entry, login_required


### Mixins ####################################################################

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

class BaseCreateView(edit.CreateView):
    """
    The used Model should have a creator and name field.
    """
    success_message = __('{name} created successfully')

    def form_valid(self, form):
        form.instance.creator = self.request.user
        self.object = form.save()

        # Display success message
        name = form.cleaned_data['name']
        msg = self.success_message.format(name=name)
        messages.success(self.request, msg)

        create_log_entry(self.object, self.request.user, ADDITION)

        return HttpResponseRedirect(self.get_success_url())


class BaseUpdateView(FilterCreatorMixin, edit.UpdateView):
    """
    The used Model should have a creator and name field.
    """
    success_message = __('{name} updated successfully')

    def form_valid(self, form):
        self.object = form.save()

        # Display success message
        name = self.object.name
        msg = self.success_message.format(name=name)
        messages.success(self.request, msg)

        create_log_entry(self.object, self.request.user, CHANGE)

        return HttpResponseRedirect(self.get_success_url())


class BaseDeleteView(FilterCreatorMixin, edit.DeleteView):
    """
    DeleteView with user filter and redirect to Overview.

    The used Model should have a creator and name field.
    """
    success_message = __('{name} deleted successfully')
    template_name = 'charge/object_confirm_delete.html'

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.object.delete()

        # Display success message
        name = self.object.name
        msg = self.success_message.format(name=name)
        messages.success(self.request, msg)

        create_log_entry(self.object, self.request.user, DELETION)

        return HttpResponseRedirect(self.get_success_url())


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


@login_required
class EventHistory(list.ListView):
    model = models.EventLogEntry
    template_name = 'charge/event_history.html'

    def get_queryset(self):
        event_pk = self.kwargs['pk']
        item_ids = models.Item.objects.filter(event__in=event_pk).values_list(
                'id', flat=True)
        event_ct = ContentType.objects.get_for_model(models.Event)
        event_filter = Q(content_type=event_ct, object_id=event_pk)
        item_ct = ContentType.objects.get_for_model(models.Item)
        item_filter = Q(content_type=item_ct, object_id__in=item_ids)
        qs = self.model.objects.filter(event_filter | item_filter)
        return qs


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

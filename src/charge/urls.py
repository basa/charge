# -*- coding: utf-8 -*-

from django.conf import settings
from django.conf.urls import patterns, url
from django.contrib.auth import views as auth_views
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.views.generic import DetailView, ListView, TemplateView

from charge.forms import AuthenticationForm, RegistrationForm
from charge.models import Event
from charge.views import EventCreate, EventUpdate, EventDelete


urlpatterns = patterns('',
    url(r'^$', TemplateView.as_view(template_name='index.html'), name='index'),

    # django-registration
    url(r'^login/$', auth_views.login,
            {'authentication_form': AuthenticationForm,
             'template_name': 'registration/login.html'}, name='auth_login'),
    url(r'^register/$', 'registration.views.register',
            {'backend': 'registration.backends.simple.SimpleBackend',
             'form_class': RegistrationForm,
             'success_url': 'events'}, name='registration_register'),

    # events
    url(r'^events/$', ListView.as_view(model=Event), name='events'),
    url(r'^event/add/$', EventCreate.as_view(), name='event_add'),
    url(r'^event/(?P<pk>\d+)/$', DetailView.as_view(model=Event),
            name='event'),
    url(r'^event/(?P<pk>\d+)/update/$', EventUpdate.as_view(),
            name='event_update'),
    url(r'^event/(?P<pk>\d+)/delete/$', EventDelete.as_view(),
            name='event_delete'),

    # items
)

if settings.DEBUG:
    urlpatterns += staticfiles_urlpatterns()

# -*- coding: utf-8 -*-

from django.conf import settings
from django.conf.urls import include, patterns, url
from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.views.generic import DetailView, TemplateView

from charge.forms import AuthenticationForm, RegistrationForm
from charge.models import Item
from charge.views import (EventCreate, EventDelete, EventDetail, EventUpdate,
        ItemCreate, ItemDelete, ItemUpdate, Logout, Overview)


admin.autodiscover()


urlpatterns = patterns('',
    # django.contrib.admin
    (r'^admin/', include(admin.site.urls)),

    url(r'^$', TemplateView.as_view(template_name='index.html'), name='index'),

    # django.contrib.auth
    url(r'^login/$', auth_views.login,
            {'authentication_form': AuthenticationForm,
             'template_name': 'registration/login.html'}, name='auth_login'),
    url(r'^logout/$', Logout.as_view(), name='auth_logout'),
    # django-registration
    url(r'^register/$', 'registration.views.register',
            {'backend': 'registration.backends.simple.SimpleBackend',
             'form_class': RegistrationForm,
             'success_url': 'overview'}, name='registration_register'),

    # Event related
    url(r'^event/add/$', EventCreate.as_view(), name='event_add'),
    url(r'^event/(?P<pk>\d+)/$', EventDetail.as_view(), name='event'),
    url(r'^event/(?P<pk>\d+)/update/$', EventUpdate.as_view(),
            name='event_update'),
    url(r'^event/(?P<pk>\d+)/delete/$', EventDelete.as_view(),
            name='event_delete'),

    # Item related
    url(r'^item/add/$', ItemCreate.as_view(), name='item_add'),
    url(r'^item/(?P<pk>\d+)/$', DetailView.as_view(model=Item),
            name='item'),
    url(r'^item/(?P<pk>\d+)/update/$', ItemUpdate.as_view(),
            name='item_update'),
    url(r'^item/(?P<pk>\d+)/delete/$', ItemDelete.as_view(),
            name='item_delete'),
            
    # Event/Comments related
    url(r'^comments/', include('django.contrib.comments.urls')),

    # user
    url(r'^overview/$', Overview.as_view(), name='overview'),
)

if settings.DEBUG:
    urlpatterns += staticfiles_urlpatterns()

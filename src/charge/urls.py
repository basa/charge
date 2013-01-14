# -*- coding: utf-8 -*-

from django.conf.urls import patterns, url
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.views.generic import ListView, TemplateView

from charge.models import Event
from charge.views import EventCreate, EventUpdate, EventDelete


urlpatterns = patterns('',
    url(r'^$', TemplateView.as_view(template_name='index.html'), name='index'),
    # events
    url(r'^events/$', ListView.as_view(model=Event), name='events'),
    url(r'event/add/$', EventCreate.as_view(), name='event_add'),
    url(r'event/(?P<pk>\d+)/$', EventUpdate.as_view(), name='event_update'),
    url(r'event/(?P<pk>\d+)/delete/$', EventDelete.as_view(),
            name='event_delete'),
)

urlpatterns += staticfiles_urlpatterns()

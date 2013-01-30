# -*- coding: utf-8 -*-

from django.conf import settings
from django.conf.urls import include, patterns, url
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.views.generic import TemplateView

from charge.forms import AuthenticationForm, RegistrationForm
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
    url(r'^item/add/(?P<event_pk>\d+)/$', ItemCreate.as_view(),
            name='item_add'),
    url(r'^item/(?P<pk>\d+)/update/$', ItemUpdate.as_view(),
            name='item_update'),
    url(r'^item/(?P<pk>\d+)/delete/$', ItemDelete.as_view(),
            name='item_delete'),

    # Event/Comments related
    (r'^comments/', include('django.contrib.comments.urls')),

    # user
    url(r'^overview/$', Overview.as_view(), name='overview'),
    url(r'^users/(?P<user>\w+)/$', 'charge.views.user', name='user'),

    # i18n
    (r'^i18n/', include('django.conf.urls.i18n')),

    # django-rosetta
    (r'^rosetta/', include('rosetta.urls')),
) + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

if settings.DEBUG:
    urlpatterns += staticfiles_urlpatterns()

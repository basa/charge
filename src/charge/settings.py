# -*- coding: utf-8 -*-
import os

from django.core.urlresolvers import reverse_lazy


PROJECT_ROOT = os.path.abspath(os.path.dirname(__file__))
MEDIA_ROOT = PROJECT_ROOT + '/../../var/media/'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': 'var/db'
    }
}

INSTALLED_APPS = [
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.messages',
    'django.contrib.sessions',
    'django.contrib.admin',
    'django.contrib.staticfiles',
    'django.contrib.sites',
    'django.contrib.comments',
    'bootstrap',
    'registration',
    'charge',
    'my_comments',
]

COMMENTS_APP = 'my_comments'

ROOT_URLCONF = 'charge.urls'
LOGIN_URL = reverse_lazy('auth_login')
LOGIN_REDIRECT_URL = reverse_lazy('overview')

SITE_ID = 1

TEMPLATE_DIRS = (
    os.path.join(PROJECT_ROOT, 'templates'),
)
TEMPLATE_CONTEXT_PROCESSORS = (
    'django.core.context_processors.debug',
    'django.core.context_processors.i18n',
    'django.core.context_processors.media',
    'django.core.context_processors.static',
    'django.contrib.auth.context_processors.auth',
    'django.contrib.messages.context_processors.messages',
)
STATIC_URL = '/static/'
MEDIA_URL = '/media/'

MIDDLEWARES = (
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
)

DEBUG = True

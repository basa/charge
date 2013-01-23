# -*- coding: utf-8 -*-

from django.contrib.auth.decorators import (login_required as
        auth_login_required)
from django.utils.decorators import method_decorator


def login_required(cls=None, **login_args):
    """
    Apply the login_required decorator to all the handlers in a class-based
    view that delegate to the dispatch method.

    Optional Args:
        redirect_field_name: Default is django.contrib.auth.REDIRECT_FIELD_NAME
        login_url: Default is None

    See the documentation for the login_required for more information
    about the keyword arguments.

    Usage:
      @LoginRequired
      class MyListView (ListView):
    """
    if cls is not None:
        # Check that the View class is a class-based view. This can either be
        # done by checking inheritance from django.views.generic.View, or by
        # checking that the ViewClass has a ``dispatch`` method.
        if not hasattr(cls, 'dispatch'):
            raise TypeError(('View class is not valid: %r.  Class-based views '
                             'must have a dispatch method.') % cls)

        decoratored_dispatch = method_decorator(
                auth_login_required(**login_args))(cls.dispatch)
        cls.dispatch = decoratored_dispatch

        return cls

    else:
        # If ViewClass is None, then this was applied as a decorator with
        # parameters. An inner decorator will be used to capture the ViewClass,
        # and return the actual decorator method.
        def inner_decorator(inner_cls):
            return login_required(inner_cls, **login_args)

        return inner_decorator

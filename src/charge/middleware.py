# -*- coding: utf-8 -*-
from django.contrib import messages
from django.contrib.auth import logout
from django.core.urlresolvers import NoReverseMatch, reverse


class AdminLogout(object):
    def process_request(self, request):
        user = request.user
        if user.is_authenticated() and user.is_staff:
            try:
                admin_index = reverse('admin:index')
            except NoReverseMatch:
                return
            if not request.path.startswith(admin_index):
                logout(request)
                messages.info(request, 'Staff user are for admin only.',
                        fail_silently=True)

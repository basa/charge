# -*- coding: utf-8 -*-

from django.contrib.admin.models import ADDITION, CHANGE, DELETION


def post_delete(sender, instance, *kwargs):
    instance._create_log_entry(DELETION)


def post_save(sender, instance, created, *kwargs):
    if created:
        action_flag = ADDITION
    else:
        action_flag = CHANGE
    instance._create_log_entry(action_flag)

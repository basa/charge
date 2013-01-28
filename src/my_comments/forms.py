# -*- coding: utf-8 -*-
from bootstrap.forms import BootstrapMixin, Fieldset
from django.contrib.comments.forms import CommentDetailsForm


class CommentForm(BootstrapMixin, CommentDetailsForm):
    """
    BootstrapForm for comments.

    Includes just the comment textarea and the hidden fields.
    """
    class Meta:
        layout = (
            Fieldset('Add Comment', 'comment', 'content_type', 'object_pk',
                    'timestamp', 'security_hash'),
        )

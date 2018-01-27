from django.db import models


class ModelMixin(object):
    """ model  mixin """
    added = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

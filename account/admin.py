from django.contrib import admin

from . import models

model_list = [models.User]

admin.site.register(model_list)

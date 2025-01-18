from django.contrib import admin
from . import models
# Register your models here.

admin.site.register(models.StatPool)
admin.site.register(models.StatPoolCategory)
admin.site.register(models.StatPoolUser)
admin.site.register(models.StatPoolUserPick)
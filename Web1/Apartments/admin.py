from django.contrib import admin
from . import models
# Register your models here.
admin.site.register(models.User)
admin.site.register(models.Apartment)
admin.site.register(models.Image)
admin.site.register(models.Request)



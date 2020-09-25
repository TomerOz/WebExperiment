from django.contrib import admin

# Register your models here.
from .models import ProfileModel, Feature


admin.site.register(ProfileModel)
admin.site.register(Feature)

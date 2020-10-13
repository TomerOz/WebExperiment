from django.contrib import admin

# Register your models here.
from .models import ProfileModel, FeatureLabels, FeatureValue


admin.site.register(ProfileModel)
admin.site.register(FeatureLabels)
admin.site.register(FeatureValue)

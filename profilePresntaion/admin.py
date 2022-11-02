from django.contrib import admin

# Register your models here.
from .models import ProfileModel, FeatureLabels, FeatureValue, Subject, Experiment, Instruction, ExperimentPhase, GameMatrix
from .models import Context, FeatureWeight, SimilarityContextModel

# 
# admin.site.register(ProfileModel)
# admin.site.register(FeatureLabels)
# admin.site.register(FeatureValue)
# admin.site.register(Subject)
# admin.site.register(Instruction)
# admin.site.register(Experiment)
# admin.site.register(ExperimentPhase)
# admin.site.register(GameMatrix)
# admin.site.register(Context)
# admin.site.register(FeatureWeight)
# admin.site.register(SimilarityContextModel)

from django.shortcuts import render, get_object_or_404
from .models import ProfileModel, FeatureLabels
from django.core import serializers

import json
import ipdb
import random

# Create your views here.
def index(request):
    return render(request, 'profilePresntaion/Index.html')

def get_subject_profile(request):
    #ipdb.set_trace()
    if request.method != 'POST':
        features_list = []
        for fl in FeatureLabels.objects.all():
            features_list.append([fl.feature_name, fl.right_end, fl.left_end])
        random.shuffle(features_list)

        return render(request, 'profilePresntaion/GetSubject/getSubjectProfil.html', {"features_list" : json.dumps(features_list), "features_list1" : features_list})
    else:
        #print(request.POST, request.user)
        return render(request, 'profilePresntaion/GetSubject/getSubjectProfil.html')


def present_profile(request, profile_pk):
    profile = get_object_or_404(ProfileModel, pk=profile_pk)
    all_profiles = ProfileModel.objects.all()
    context = {}
    data = serializers.serialize("json", ProfileModel.objects.all())
    context["profiles"] = data

    for profile in all_profiles:
        context[profile.id] = {}

        features_list_try = serializers.serialize("json", profile.featurevalue_set.all())
        context[profile.id]["features_try"] = features_list_try

        features_list = profile.featurevalue_set.all()[::1]
        context[profile.id]["name"] = profile.name
        context[profile.id]["features"] = {}
        for f in features_list:
            f_name = f.target_feature.feature_name
            context[profile.id]["features"][f_name] = {}
            context[profile.id]["features"][f_name]["value"] = f.value
            context[profile.id]["features"][f_name]["l"] = f.target_feature.left_end
            context[profile.id]["features"][f_name]["r"] = f.target_feature.right_end

    return render(request, 'profilePresntaion/profile.html', {'context': json.dumps(context)})

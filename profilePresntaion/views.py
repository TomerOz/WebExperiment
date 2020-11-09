from django.shortcuts import render, get_object_or_404
from .models import ProfileModel, FeatureLabels, Subject, FeatureValue, Experiment
from django.core import serializers

import json
import ipdb
import random

# Create your views here.
def index(request):
    if request.method == 'POST': # When consent form was filled
        return present_profile(request) # NOT HERE - THIS FUNCTION SHOULD BE MOVED
    else: # Rendering consent form "Index.html"
        subject = _get_user_subject(request.user) # Why is this here?
        return render(request, 'profilePresntaion/Index.html', {"subject": subject.pk})

# New subject - creating his/her new progile:
def get_subject_profile(request):
    if request.method != 'POST': # On starting to add new subject profile
        features_list = []
        for fl in FeatureLabels.objects.all():
            features_list.append([fl.feature_name, fl.right_end, fl.left_end])
        random.shuffle(features_list)

        return render(request, 'profilePresntaion/GetSubject/getSubjectProfil.html', {"features_list" : json.dumps(features_list), "features_list1" : features_list})
    else: # On saving a new subject profile
        _create_subject_profile(request.user, request.POST)
        present_profile(request) # Not necceraliy here - what should be the next page?

def _create_subject_profile(user, post_data): # Fills subject model with posted features provided by the subject user
    new_subject = _get_user_subject(user)
    new_subject.featurevalue_set.all().delete() # deeleting existing features data on this profile if re-entered
    feaure_labels = FeatureLabels.objects.values_list("feature_name", flat=True)
    for feature_name in feaure_labels:
        feature = FeatureLabels.objects.get(feature_name=feature_name)
        feature_value = int(post_data[feature_name])
        subject_feature = FeatureValue(target_profile=new_subject, target_feature=feature, value=feature_value)
        subject_feature.save()
    new_subject.save(force_update=True)

def _create_subject(user):
    new_subject = Subject(experiment=Experiment.objects.get(name="SGS1"))
    new_subject.save()
    new_subject.is_subject = True
    new_subject.name = "Subject-"+str(new_subject.pk)
    new_subject.save(force_update=True)
    user.exp1_enc_num = str(new_subject.pk)
    user.save()
    return new_subject

def _get_user_subject(user):
    if _check_if_user_have_subject(user):
        subject = Subject.objects.get(pk=user.exp1_enc_num)
    else:
        subject = _create_subject(user)
    return subject
        # a need to create a subject..

def _check_if_user_have_subject(user):
    if user.exp1_enc_num != "": # check if not empty
        if user.exp1_enc_num.isdigit(): # check if its int
            if Subject.objects.filter(pk=user.exp1_enc_num).exists(): # check if encrypted number represent a valid pk in Subject
                return True
    return False

def present_profile(request):
    # profile = get_object_or_404(ProfileModel, pk=profile_pk)
    all_profiles = ProfileModel.objects.all()
    context = {}

    # Check if following lines are ok for scecurity (e.g. passing actuall other subjects data to current subject)
    # data = serializers.serialize("json", ProfileModel.objects.all())
    # context["profiles"] = data

    context["profiles_list"] = [] # This is the list the will be iterated through the experiment

    for profile in all_profiles:
        if not profile.is_subject:
            context[profile.id] = {}
            context["profiles_list"].append(profile.id)

            features_list = profile.featurevalue_set.all()[::1]
            context[profile.id]["name"] = profile.name
            context[profile.id]["is_subject"] = profile.is_subject
            context[profile.id]["features"] = {}
            for f in features_list:
                f_name = f.target_feature.feature_name
                context[profile.id]["features"][f_name] = {}
                context[profile.id]["features"][f_name]["value"] = f.value
                context[profile.id]["features"][f_name]["l"] = f.target_feature.left_end
                context[profile.id]["features"][f_name]["r"] = f.target_feature.right_end

    subject = Subject.objects.get(pk=request.user.exp1_enc_num)
    context["subject"] = "is subject = " + str(subject.is_subject) + " "  + str(subject.pk)
    random.shuffle(context["profiles_list"])
    return render(request, 'profilePresntaion/profile.html', {'context': json.dumps(context)})

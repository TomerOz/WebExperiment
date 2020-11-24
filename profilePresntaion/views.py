from django.shortcuts import render, get_object_or_404
from .models import ProfileModel, FeatureLabels, Subject, FeatureValue, Experiment, Instruction
from django.core import serializers

import json
import ipdb
import random

from .myUtils.FormsProcessing import FormsProcessor, PhasesDataSaver

sgs1_phases = ["Consent phase", "Pre Task",
            "Pre Get Profile", "During Get Profile",
            "Pre Profile Presentation", "Pre Task", "During Profile Presentation",
            "Pre Game", "During Game"]

phase_to_html_page = {
                        "Consent phase":                "Index",
                        "Pre Task":                     "instruction",
                        "Pre Get Profile":              "instruction",
                        "During Get Profile":           "GetSubject\getSubjectProfile",
                        "Pre Profile Presentation":     "instruction",
                        "During Profile Presentation":  "profile",
                        "Pre Game":                     "instruction",
                        "During Game":                  "profile",
                    }

form_phase = "form_phase"

forms_processor = FormsProcessor()
phases_data_saver = PhasesDataSaver(FeatureLabels, FeatureValue)

# saves subject model with the new phase
def _update_subject_phase(subject):
    subject_updated_phase = _get_next_phase(subject)
    subject.current_phase = subject_updated_phase
    subject.save()

 # return a query set of all phases-model instances associated with this subject's experiment
def _get_all_subject_phases(subject):
    return subject.experiment.experimentphase_set.all()

# returns the name of next phase of this subject
def _get_next_phase(subject):
    next_phase_index = sgs1_phases.index(subject.current_phase) + 1
    if next_phase_index < len(sgs1_phases):
        return sgs1_phases[next_phase_index]
    else:
        return Exception("reached last phase")

# returns a list all instruciton-model instances texts associated with this phase - orderd by order property
def _get_phases_instructions(phase_name):
    instructions_list = []
    instruction_queryset = Instruction.objects.filter(str_phase__name = phase_name).order_by("int_place")
    for instruction_query in instruction_queryset:
        instructions_list.append(instruction_query.instruction_text)
    return instructions_list

# creates a  BLANK Subject model instance and associtates it with ForeignKey to the authenticated user
def _create_subject(user):
    new_subject = Subject(experiment=Experiment.objects.get(name="SGS1"))
    new_subject.save()
    new_subject.is_subject = True
    new_subject.name = "Subject-"+str(new_subject.pk)
    new_subject.save(force_update=True)
    user.exp1_enc_num = str(new_subject.pk)
    user.save()
    return new_subject

# return the Subject instance associated with the authenticated user
def _get_user_subject(user):
    if _check_if_user_have_subject(user):
        subject = Subject.objects.get(pk=user.exp1_enc_num)
    else: # a need to create a subject..
        subject = _create_subject(user)
    return subject

# returns a boolean depending on whether user has an associated Subject instance
def _check_if_user_have_subject(user):
    context = ""
    if user.exp1_enc_num != "": # check if not empty
        if user.exp1_enc_num.isdigit(): # check if its int
            if Subject.objects.filter(pk=user.exp1_enc_num).exists(): # check if encrypted number represent a valid pk in Subject
                return True
    return False

# returns a context dictionary withh all the profiles data ready for rendering (a sort od serialiser)
def _get_profiles_list_context(all_profiles):
    profiles_data = {}
    profiles_data["profiles_list"] = [] # This is the list the will be iterated through the experiment

    for profile in all_profiles:
        if not profile.is_subject:
            profiles_data[profile.id] = {}
            profiles_data["profiles_list"].append(profile.id)

            features_list = profile.featurevalue_set.all()[::1]
            profiles_data[profile.id]["name"] = profile.name
            profiles_data[profile.id]["is_subject"] = profile.is_subject
            profiles_data[profile.id]["features"] = {}
            for f in features_list:
                f_name = f.target_feature.feature_name
                profiles_data[profile.id]["features"][f_name] = {}
                profiles_data[profile.id]["features"][f_name]["value"] = f.value
                profiles_data[profile.id]["features"][f_name]["l"] = f.target_feature.left_end
                profiles_data[profile.id]["features"][f_name]["r"] = f.target_feature.right_end
    return profiles_data

# Preparing context for the a new subject page
def _get_new_subject_profile_page_context():
    features_list = []
    for fl in FeatureLabels.objects.all():
        features_list.append([fl.feature_name, fl.right_end, fl.left_end])
    random.shuffle(features_list)
    return {"features_list" : json.dumps(features_list)}


# Initiation of profiles presentation phase - renders all profiles as JSON, each profile presentation is manged via js
def get_page_present_profile(request, phase_code):
    profiles_data = _get_profiles_list_context(ProfileModel.objects.all())
    random.shuffle(profiles_data["profiles_list"])
    context = {form_phase: phase_code, 'context': json.dumps(profiles_data)}
    return render(request, 'profilePresntaion/profile.html', context)


def render_next_phase(request, users_subject):
    errors = None # a place holder for errors
    if request.method == "POST":
        errors = forms_processor.process_form(users_subject.current_phase, request.POST)
        phases_data_saver.save_posted_data(users_subject.current_phase, request.POST, users_subject)
        if (len(errors) == 0) & (request.POST[form_phase] == users_subject.current_phase):
            # condition fails on errors or GET (user was sent from home page with a get method) or
            #in case of page refresh request.POST is previous phasewhile users_subject.current_phase moved forward
            _update_subject_phase(users_subject) # updates "users_subject.current_phase"
    phases_instructions = _get_phases_instructions(users_subject.current_phase)
    single_instruction = phases_instructions[0] if len(phases_instructions) == 1 else None
    context = {"form_phase": users_subject.current_phase,
                "instructions_list":  json.dumps(phases_instructions),
                "errors":errors,
                "single_instructions": single_instruction}

    if users_subject.current_phase == "During Get Profile":
        context.update(_get_new_subject_profile_page_context())

    return render(request, 'profilePresntaion/{}.html'.format(phase_to_html_page[users_subject.current_phase]), context)

# A general function that serves as phase decider
def get_phase_page(request):
    users_subject = _get_user_subject(request.user)
    # TODO: Make sure user is authenticated.. subject is ready --> maybe already take care for
    # TODO: Make sure subject did not already finished this expperiment
    # TODO: maybe make user subject creation be mediated by a mail an a manual connection (no in DB)
    return render_next_phase(request, users_subject)

    # New subject profile page -- > this view is kept seprately for development purposes
    # New subject - creating his/her new progile:
def get_page_get_subject_profile(request, phase_code):
    if request.method != 'POST': # On starting to add new subject profile
        features_list = []
        for fl in FeatureLabels.objects.all():
            features_list.append([fl.feature_name, fl.right_end, fl.left_end])
        random.shuffle(features_list)
        context = {form_phase: phase_code, "features_list" : json.dumps(features_list)}
        return render(request, 'profilePresntaion/GetSubject/getSubjectProfile.html', context)
    else: # On saving a new subject profile
        _create_subject_profile(request.user, request.POST)
        get_page_present_profile(request, phase_code) # Not necceraliy here - what should be the next page?



# def index(request):
#     ipdb.set_trace()
#     if request.method == 'POST': # When consent form was filled
#         return get_page_present_profile(request) # NOT HERE - THIS FUNCTION SHOULD BE MOVED
#     else: # Rendering consent form "Index.html"
#         subject = _get_user_subject(request.user) # Why is this here?
#         return render(request, 'profilePresntaion/Index.html', {"subject": subject.pk})

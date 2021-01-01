from django.shortcuts import render, redirect, reverse, get_object_or_404
from .models import ProfileModel, FeatureLabels, Subject, FeatureValue, Experiment, Instruction, GameMatrix
from django.core import serializers

import json
import ipdb
import random

from .myUtils.FormsProcessing import FormsProcessor, PhasesDataSaver

sgs1_phases = ["Consent phase", "Pre Task",
            "Pre Get Profile", "During Get Profile", "Matrix tutorial",
            "Pre Profile Presentation", "During Profile Presentation",
            "end"]

phase_to_html_page = {
                        "Consent phase":                "Index",
                        "Pre Task":                     "instruction",
                        "Pre Get Profile":              "instruction",
                        "During Get Profile":           "GetSubject/getSubjectProfile",
                        "Matrix tutorial":              "MatrixLearnTest",
                        "Pre Profile Presentation":     "instruction",
                        "During Profile Presentation":  "profile",
                        "end":                          "endPage",
                    }

form_phase = "form_phase"

forms_processor = FormsProcessor()
phases_data_saver = PhasesDataSaver(FeatureLabels, FeatureValue)

## Assistant functions: ###############################################################################################################################################
# saves subject model with the new phase
def _update_subject_phase(subject):
    subject_updated_phase = _get_next_phase(subject)
    subject.current_phase = subject_updated_phase
    subject.save()
    if subject_updated_phase == "end of experiment":
        subject.update_subject_session_on_complete()


 # return a query set of all phases-model instances associated with this subject's experiment
def _get_all_subject_phases(subject):
    return subject.experiment.experimentphase_set.all()

# returns the name of next phase of this subject
def _get_next_phase(subject):
    next_phase_index = sgs1_phases.index(subject.current_phase) + 1
    #if next_phase_index < len(sgs1_phases):
    if next_phase_index < 7: # temporary hardcoded
        return sgs1_phases[next_phase_index]
    else:
        return "end of experiment"

# returns a list all instruciton-model instances texts associated with this phase - orderd by order property
def _get_phases_instructions(phase_name):
    instructions_list = []
    instruction_queryset = Instruction.objects.filter(str_phase__name=phase_name, is_in_order=True).order_by("int_place")
    for instruction_query in instruction_queryset:
        instructions_list.append(instruction_query.instruction_text)
    return instructions_list

# creates a  BLANK Subject model instance and associtates it with ForeignKey to the authenticated user
def _create_subject(user):
    new_subject = Subject(experiment=Experiment.objects.get(name="SGS1"))
    new_subject.save()
    new_subject.is_subject = True
    new_subject.name = "Subject-"+str(new_subject.pk)
    new_subject.subject_session = 1 # on creation subject session is one
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

    random.shuffle(profiles_data["profiles_list"])
    return profiles_data

# Preparing context for the a new subject page
def _get_new_subject_profile_page_context():
    features_list = []
    for fl in FeatureLabels.objects.all():
        features_list.append([fl.feature_name, fl.right_end, fl.left_end])
    random.shuffle(features_list)
    return {"features_list" : json.dumps(features_list)}

# Builds a generic context that is used in all views
def _get_context(form_phase, instructions_list, single_instruction_text, errors):
    context = {
                "form_phase": form_phase,
                "instructions_list":  json.dumps(instructions_list),
                "single_instructions": single_instruction_text,
                "errors":errors,
                }
    return context

# Updates the generic context on specific phases
def _update_context_if_necessry(context, current_phase, users_subject):
    if current_phase == "During Get Profile":
        context.update(_get_new_subject_profile_page_context())

    elif current_phase == "Matrix tutorial":
        game = _get_game_data(users_subject)
        gameJSON = json.dumps(_get_game_dict(game))
        context.update({"game":game,
                        "gameJSON":gameJSON,
                        })
    elif current_phase == "During Profile Presentation":
        game = _get_game_data(users_subject)
        gameJSON = json.dumps(_get_game_dict(game))
        context.update({"context":json.dumps(_get_profiles_list_context(ProfileModel.objects.all())),
                        "game":game,
                        "gameJSON":gameJSON,
                        })
    return context # if condition fails, context remain untouched
def _get_enriched_instructions_if_nesseccary(subject, phases_instructions, single_instruction):
    if subject.current_phase == "Matrix tutorial":
        game = _get_game_data(subject)
        phases_instructions[0] = phases_instructions[0].format(game.strategy_a,game.strategy_b)
    return phases_instructions, single_instruction

def _get_game_data(subject):
    # How it will look once models are updaed:
    # game = GameMatrix.objects.filter(context=subject.context_group, ps=subject.session_to_ps)
    game = GameMatrix.objects.filter(phase__name=subject.current_phase)[0]
    return game

def _get_game_dict(game):
    game_dict = {}
    game_dict["A"] = game.strategy_a
    game_dict["B"] = game.strategy_b
    game_dict["pA_Aa"] = game.pA_Aa
    game_dict["pB_Aa"] = game.pB_Aa
    game_dict["pA_Ab"] = game.pA_Ab
    game_dict["pB_Ab"] = game.pB_Ab
    game_dict["pA_Ba"] = game.pA_Ba
    game_dict["pB_Ba"] = game.pB_Ba
    game_dict["pA_Bb"] = game.pA_Bb
    game_dict["pB_Bb"] = game.pB_Bb

    return game_dict

## Experiment Views: ################################################################################################################################################
def render_next_phase(request, users_subject):
    errors = None # a place holder for errors
    if request.method == "POST":
        errors = forms_processor.process_form(users_subject.current_phase, request.POST)
        phases_data_saver.save_posted_data(users_subject.current_phase, request.POST, users_subject)
        if (len(errors) == 0) & (request.POST[form_phase] == users_subject.current_phase):
            # condition fails on errors or GET (user was sent from home page with a get method) or
            #in case of page refresh request.POST is previous phasewhile users_subject.current_phase moved forward
            _update_subject_phase(users_subject) # updates "users_subject.current_phase"
            if users_subject.current_phase == "end of experiment":
                return redirect(reverse('home:home')) # temporary - SHOULD HAVE ITS OWN END PAGE (FEEDBACK)
    phases_instructions = _get_phases_instructions(users_subject.current_phase)
    single_instruction = phases_instructions[0] if len(phases_instructions) == 1 else None
    phases_instructions, single_instruction = _get_enriched_instructions_if_nesseccary(users_subject, phases_instructions, single_instruction)
    context = _get_context(users_subject.current_phase, phases_instructions, single_instruction, errors)
    context = _update_context_if_necessry(context, users_subject.current_phase, users_subject)

    return render(request, 'profilePresntaion/{}.html'.format(phase_to_html_page[users_subject.current_phase]), context)

# A general function that serves as phase decider
def get_phase_page(request):
    users_subject = _get_user_subject(request.user)
    # TODO: Make sure user is authenticated.. subject is ready --> maybe already take care for
    # TODO: Make sure subject did not already finished this expperiment
    # TODO: maybe make user subject creation be mediated by a mail an a manual connection (no in DB)
    return render_next_phase(request, users_subject)

## Development Views: ################################################################################################################################################
# New subject profile page -- > this view is kept seprately for development purposes, New subject - creating his/her new progile:
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
        get_page_present_profile(request, phase_code)
# A view that mediates profile presentation to the subject
def get_page_present_profile(request, phase_code):
    profiles_data = _get_profiles_list_context(ProfileModel.objects.all())
    context = {form_phase: phase_code, 'context': json.dumps(profiles_data)}
    return render(request, 'profilePresntaion/profile.html', context)
# consent form view
def index(request):
    if request.method == 'POST': # When consent form was filled
        return get_page_present_profile(request) # NOT HERE - THIS FUNCTION SHOULD BE MOVED
    else: # Rendering consent form "Index.html"
        subject = _get_user_subject(request.user) # Why is this here?
        return render(request, 'profilePresntaion/Index.html', {"subject": subject.pk})

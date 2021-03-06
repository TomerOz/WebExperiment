from django.shortcuts import render, redirect, reverse, get_object_or_404
from .models import ProfileModel, FeatureLabels, Subject, FeatureValue, Experiment
from .models import Instruction, GameMatrix, ExperimentPhase, SimilarityContextModel
from .models import Context
from django.core import serializers

import json
import ipdb
import random
import copy

from .myUtils.FormsProcessing import FormsProcessor, PhasesDataSaver

phase_to_html_page = {
                        "Consent phase":                "Index",
                        "Pre Task":                     "instruction",
                        "Pre Get Profile":              "instruction",
                        "During Get Profile":           "GetSubject/getSubjectProfile",
                        "Pre Identification Task":      "instruction",
                        "Identification Task":           "IdentificationTask",
                        "Matrix tutorial":              "MatrixLearnTest",
                        "Pre Profile Presentation":     "instruction",
                        "During Profile Presentation":  "profile",
                        "end":                          "endPage",
                    }

form_phase = "form_phase"

forms_processor = FormsProcessor(GameMatrix)
phases_data_saver = PhasesDataSaver(FeatureLabels, FeatureValue)

## Assistant functions: ###############################################################################################################################################
# saves subject model with the new phase
def _update_subject_phase(subject):
    subject_updated_phase = _get_next_phase(subject)
    subject.current_phase = subject_updated_phase
    subject.save()
    if subject_updated_phase == "end":
        subject.update_subject_session_on_complete()

 # return a query set of all phases-model instances associated with this subject's experiment
def _get_all_subject_phases(subject):
    return subject.experiment.experimentphase_set.all()

# returns the name of next phase of this subject
def _get_next_phase(subject):
    phases = ExperimentPhase.objects.all()
    if subject.current_phase.name != "end":
        next_phase = phases.get(phase_place=subject.current_phase.phase_place+1)
        return next_phase
    else: # upon ening a session
        return "session end"

# returns a list all instruciton-model instances texts associated with this phase - orderd by order property
def _get_phases_instructions(phase_name):
    instructions_list = []
    instruction_queryset = Instruction.objects.filter(str_phase__name=phase_name, is_in_order=True).order_by("int_place")
    for instruction_query in instruction_queryset:
        instructions_list.append(instruction_query.instruction_text)

    off_order_instructions_dict = {}
    off_order_instruction_queryset = Instruction.objects.filter(str_phase__name=phase_name, is_in_order=False)
    for instruction_query in off_order_instruction_queryset:
        off_order_instructions_dict[instruction_query.off_order_place] = instruction_query.instruction_text

    return instructions_list, off_order_instructions_dict

# Returns one of the contexts
def _get_random_context():
    contexts = ["trade", "conflict", "romantic","friendship"]
    return contexts[random.randint(0, len(contexts)-1)] # temporary - TODO: monitro with db maybe via the Experiment model

# Returns the current session ps
def _get_sessions_ps(context):
    rand_i = random.randint(0, 1) # temporary - TODO: monitro with db maybe via the Experiment model
    other_i =(rand_i - 1) * -1
    subjects_context = Context.objects.get(name=context)
    games = GameMatrix.objects.filter(context_group=subjects_context) # assuming only tow games Ps* per context
    pss = (games[rand_i].ps_threshold, games[other_i].ps_threshold)
    return pss

# creates a  BLANK Subject model instance and associtates it with ForeignKey to the authenticated user
def _create_subject(user):
    new_subject = Subject(experiment=Experiment.objects.get(name="SGS1"))
    new_subject.save()
    new_subject.is_subject = True
    new_subject.name = "Subject-"+str(new_subject.pk)
    new_subject.subject_session = 1 # on creation subject session is one
    new_subject.context_group = _get_random_context()
    new_subject.session_1_ps, new_subject.session_2_ps = _get_sessions_ps(new_subject.context_group)
    new_subject.current_phase = ExperimentPhase.objects.get(name="Consent phase")
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

            features_list = profile.featurevalue_set.all()[::1] # the [::1] converts the query set into a list
            profiles_data[profile.id]["name"] = profile.name
            profiles_data[profile.id]["is_subject"] = profile.is_subject
            profiles_data[profile.id]["features"] = {}
            profiles_data[profile.id]["features_order"] = []
            for f in features_list:
                f_name = f.target_feature.feature_name
                profiles_data[profile.id]["features_order"].append(f_name)
                profiles_data[profile.id]["features"][f_name] = {}
                profiles_data[profile.id]["features"][f_name]["value"] = f.value
                profiles_data[profile.id]["features"][f_name]["l"] = f.target_feature.left_end
                profiles_data[profile.id]["features"][f_name]["r"] = f.target_feature.right_end
            random.shuffle(profiles_data[profile.id]["features_order"])

    random.shuffle(profiles_data["profiles_list"])
    return profiles_data

# Preparing context for the a new subject page
def _get_new_subject_profile_page_context():
    features_list = []
    for fl in FeatureLabels.objects.get(label_set="B").all():
        features_list.append([fl.feature_name, fl.right_end, fl.left_end])
    random.shuffle(features_list)
    return {"features_list" : json.dumps(features_list)}

# Builds a generic context that is used in all views (db-html-js context, not manipulated context)
def _get_context(form_phase, instructions_list, single_instruction_text, off_order_instructions, errors):
    context = {
                "form_phase": form_phase,
                "instructions_list":  json.dumps(instructions_list),
                "off_order_instructions_dict": off_order_instructions,
                "single_instructions": single_instruction_text,
                "errors": errors,
                "errorsJSON": json.dumps(errors),
                }
    return context


def _get_subject_profile(users_subject):
    user_profile = ProfileModel.objects.get(name = users_subject.name)
    user_profile_data = {"features": {}, "features_order": [], "name": user_profile.name, "is_subject": user_profile.is_subject}
    features_data = user_profile.featurevalue_set.all()[::1] # the [::1] converts the query set into a list
    for feature in features_data:
        f_name = feature.target_feature.feature_name
        user_profile_data["features_order"].append(f_name)
        user_profile_data["features"][f_name] = {}
        user_profile_data["features"][f_name]["value"] = feature.value
        user_profile_data["features"][f_name]["l"] = feature.target_feature.left_end
        user_profile_data["features"][f_name]["r"] = feature.target_feature.right_end

    random.shuffle(user_profile_data["features_order"])
    return user_profile_data

def _get_inital_artificial_profile(user_profile_data):
    profile = copy.deepcopy(user_profile_data)
    random.shuffle(profile["features_order"]) ## Maybe should be in the same order
    profile["is_subject"] = False
    profile["name"] = "artificial"

    for f_name in user_profile_data["features"]:
        profile["features"][f_name]
        profile["features"][f_name]["value"] = random.randint(0,100)

    return profile

def _get_feature_distance_dict(subject_profile, other_profile):
    distances_dict = {}
    for f_name in subject_profile["features"]:
        d = abs(subject_profile["features"][f_name]["value"] - other_profile["features"][f_name]["value"])
        distances_dict[f_name] = d
    return distances_dict

def _get_subject_other_similarity(model, sp, ap):
    similarity = 0
    for f_name in sp["features"]:
         s_value = sp["features"][f_name]["value"] # subject profile
         a_value = ap["features"][f_name]["value"] # artificial profile
         w = model.featureweight_set.get(feature_label__feature_name=f_name).value
         similarity += w * abs(s_value - a_value)

def _get_min_similarity(model, subject_profile):
    similarity = 0
    for f_name in subject_profile["features"]:
         value = subject_profile["features"][f_name]["value"]
         distance = (100-value if value<=50 else value)/100
         w = model.featureweight_set.get(feature_label__feature_name=f_name).value
         similarity += w*distance
    return 1-similarity

def _generate_profile(users_subject, target_similarity):
    sp = _get_subject_profile(users_subject) # subject profile
    ap = _get_inital_artificial_profile(sp) # artificial profile
    model = SimilarityContextModel.objects.get(context__name=users_subject.context_group)
    min_s = _get_min_similarity(model, sp)
    adapted_target_s = (target_similarity * 100 * (1-min_s)) + min_s
    distances_dict = _get_feature_distance_dict(sp, ap)
    #ipdb.set_trace()
    return ap




    ################## Continue here #############################
    pass


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
        context.update({"context":json.dumps(_get_profiles_list_context(ProfileModel.objects.get(profile_label_set="B").all())),
                        "game":game,
                        "gameJSON":gameJSON,
                        })
    elif current_phase == "Identification Task":
        context.update({"context":json.dumps(_get_profiles_list_context(ProfileModel.objects.all()))})
        ap = _generate_profile(users_subject, 0.2)
        ap2 = _generate_profile(users_subject, 0.3)
        ap3 = _generate_profile(users_subject, 0.4)
        ap4 = _generate_profile(users_subject, 0.5)
        ap5 = _generate_profile(users_subject, 0.6)
        sp = _get_subject_profile(users_subject)
        d2 = {"identification_task" : json.dumps({"subject": sp, "artificials": [ap, ap2, ap3, ap4, ap5]})}
        context.update(d2)
        #ipdb.set_trace()

    return context # if condition fails, context remain untouched

def _get_enriched_instructions_if_nesseccary(subject, phases_instructions, single_instruction, off_order_instructions):
    if subject.current_phase.name == "Matrix tutorial":
        game = _get_game_data(subject)
        a =game.strategy_a
        b=game.strategy_b
        phases_instructions[1] = phases_instructions[1].format(a, b, a, b, b)

        off_order_instructions["You_Aa"] = off_order_instructions["You"].format(game.strategy_a, game.strategy_a)
        off_order_instructions["You_Ab"] = off_order_instructions["You"].format(game.strategy_a, game.strategy_b)
        off_order_instructions["You_Ba"] = off_order_instructions["You"].format(game.strategy_b, game.strategy_a)
        off_order_instructions["You_Bb"] = off_order_instructions["You"].format(game.strategy_b, game.strategy_b)
        off_order_instructions["Other_Aa"] = off_order_instructions["other"].format(game.strategy_a, game.strategy_a)
        off_order_instructions["Other_Ab"] = off_order_instructions["other"].format(game.strategy_a, game.strategy_b)
        off_order_instructions["Other_Ba"] = off_order_instructions["other"].format(game.strategy_b, game.strategy_a)
        off_order_instructions["Other_Bb"] = off_order_instructions["other"].format(game.strategy_b, game.strategy_b)
    return phases_instructions, single_instruction, off_order_instructions

def _get_game_data(subject):
    # How it will look once models are updaed:
    # game = GameMatrix.objects.filter(context=subject.context_group, ps=subject.session_to_ps)
    ps_threshold = subject.session_1_ps
    if subject.subject_session == 2:
        ps_threshold = subject.session_2_ps
    if subject.current_phase.name == "Matrix tutorial":
        game = GameMatrix.objects.get(phase__name=subject.current_phase.name)
    else:
        game = GameMatrix.objects.get(phase__name=subject.current_phase.name, context_group=subject.context_group, ps_threshold=ps_threshold)
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
        errors = forms_processor.process_form(users_subject.current_phase.name, request.POST)
        errors = [] if errors == None else errors # making sure errors are provided as list
        phases_data_saver.save_posted_data(users_subject.current_phase.name, request.POST, users_subject)
        if (len(errors) == 0) & (request.POST[form_phase] == users_subject.current_phase.name):
            # condition fails on errors or GET (user was sent from home page with a get method) or
            #in case of page refresh request.POST is previous phasewhile users_subject.current_phase.name moved forward
            _update_subject_phase(users_subject) # updates "users_subject.current_phase.name"
            if users_subject.current_phase.name == "session end":
                users_subject.current_phase.name = "Consent phase"
                users_subject.save()
                return redirect(reverse('home:home')) # temporary - SHOULD HAVE ITS OWN END PAGE (FEEDBACK)
    phases_instructions, off_order_instructions = _get_phases_instructions(users_subject.current_phase.name)
    single_instruction = phases_instructions[0] if len(phases_instructions) == 1 else None
    phases_instructions, single_instruction, off_order_instructions = _get_enriched_instructions_if_nesseccary(users_subject, phases_instructions, single_instruction, off_order_instructions)
    context = _get_context(users_subject.current_phase.name, phases_instructions, single_instruction, off_order_instructions, errors)
    context = _update_context_if_necessry(context, users_subject.current_phase.name, users_subject)
    return render(request, 'profilePresntaion/{}.html'.format(phase_to_html_page[users_subject.current_phase.name]), context)

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

from django.shortcuts import render, redirect, reverse, get_object_or_404
from django.db.models import Q
from .models import ProfileModel, FeatureLabels, Subject, FeatureValue, Experiment, MinMaxProfileModel, ArtificialProfileModel
from .models import Instruction, GameMatrix, ExperimentPhase, SimilarityContextModel, ShamQuestion
from .models import Context
from django.core import serializers
import datetime
import pytz

import json
import os
import ipdb
import random
import copy
import pandas as pd

from .myUtils.FormsProcessing import FormsProcessor, PhasesDataSaver
from .myUtils.ArticialProfile import create_artificial_profile_3
from .myUtils.SubjectData import SubjectData
from .myUtils.AnalyzeData import AnalyzeData

phase_to_html_page = {
                        "Consent phase":                "Index",
                        "Pre Task":                     "instruction",
                        "Get Min Max Similarity":       "MinMaxSimilariy",
                        "Pre Get Profile":              "instruction",
                        "During Get Profile1":           "GetSubject/getSubjectProfile",
                        "During Get Profile2":           "GetSubject/getSubjectProfile",
                        "Pre Identification Task":      "instruction",
                        "Identification Task":          "IdentificationTask",
                        "Pre Get Max Profile":          "instruction",
                        "Get Max Similarity Profile":   "GetSubject/getSubjectProfile",
                        "Pre Get Min Profile":          "instruction",
                        "Get Min Similarity Profile":   "GetSubject/getSubjectProfile",
                        "Matrix tutorial":              "MatrixLearnTest",
                        "Pre Profile Presentation":     "instruction",
                        "During Profile Presentation":  "profile",
                        "Report Similariy":             "ReportSimilarity",
                        "Pre Get Ideal Profile":        "instruction",
                        "Get Ideal Profile":            "GetSubject/getSubjectProfile",
                        "Demographics":                 "Demographics",
                        "End Screen":                   "endPage",
                    }

COL_NAMES_BY_GROUP = {
    "A": ['self_way_of_speech', 'self_socio_economic', 'self_ethnicity_skin_color', 'self_personality', 'self_dress_propeties', 'self_political_affiliation', 'self_hobbies', 'self_body_size', 'self_intelligence'],
    "B": ['self_goodness', 'self_age', 'self_happiness', 'self_normality', 'self_appearnce', 'self_interest', 'self_sainity', 'self_importance', 'self_amazing'],
    "C": ['self_c1', 'self_c2', 'self_c3', 'self_c4', 'self_c5', 'self_c6', 'self_c7', 'self_c8', 'self_c9'],
}

PROFILE_COL_NAMES_BY_GROUP = {
    "A": ['profile_way_of_speech', 'profile_socio_economic', 'profile_ethnicity_skin_color', 'profile_personality', 'profile_dress_propeties', 'profile_political_affiliation', 'profile_hobbies', 'profile_body_size', 'profile_intelligence'],
    "B": ['profile_goodness', 'profile_age', 'profile_happiness', 'profile_normality', 'profile_appearnce', 'profile_interest', 'profile_sainity', 'profile_importance', 'profile_amazing'],
    "C": ['profile_c1', 'profile_c2', 'profile_c3', 'profile_c4', 'profile_c5', 'profile_c6', 'profile_c7', 'profile_c8', 'profile_c9'],
}

form_phase = "form_phase"

forms_processor = FormsProcessor(GameMatrix)
phases_data_saver = PhasesDataSaver(FeatureLabels, FeatureValue, MinMaxProfileModel)

EXPERIMENT_NAME = "ipa_2"
EXPERIMENT_FIRST_SESSION = {"ipa_1_2" : 2, "ipa_2": 1}

## Assistant functions: ###############################################################################################################################################
# saves subject model with the new phase
def _update_subject_phase(subject, direction=None):
    subject_updated_phase = _get_next_phase(subject, direction=direction)
    subject.current_phase = subject_updated_phase
    subject.save()
    if subject.current_phase.name == "Pre Task" and subject.runningLocation == "Lab":
        _update_subject_phase(subject, direction=None)

 # return a query set of all phases-model instances associated with this subject's experiment
def _get_all_subject_phases(subject):
    return subject.experiment.experimentphase_set.all()

# returns the name of next phase of this subject
def _get_next_phase(subject, direction=None):
    if direction==None:
        direction=1
    phases = ExperimentPhase.objects.all()
    next_phase = phases.get(phase_place=subject.current_phase.phase_place+(direction*1))

    if subject.current_phase.name == "End Screen": # stays in place if its current phase
            return subject.current_phase

    return next_phase

# returns a list all instruciton-model instances texts associated with this phase - orderd by order property
def _get_phases_instructions(phase_name, users_subject, errors):
    instructions_list = []
    pictures_paths = []
    instruction_queryset = Instruction.objects.filter(str_phase__name=phase_name, is_in_order=True).order_by("int_place")
    for instruction_query in instruction_queryset:
        if users_subject.gender == "male":
            instructions_list.append(instruction_query.instruction_text_male)
        elif users_subject.gender == "female":
            instructions_list.append(instruction_query.instruction_text_female)
        else:
            instructions_list.append(instruction_query.instruction_text)
        # adding the pictures paths:
        for pic_name in instruction_query.pitctures_names.split(", "):
            if pic_name=="nan":
                pictures_paths.append(pic_name)
            else:
                pictures_paths.append(r'/static/ipa_2/media/images/' + pic_name)

    off_order_instructions_dict = {}
    off_order_instruction_queryset = Instruction.objects.filter(str_phase__name=phase_name, is_in_order=False)
    for instruction_query in off_order_instruction_queryset:
        if users_subject.gender == "male":
            off_order_instructions_dict[instruction_query.off_order_place] = instruction_query.instruction_text_male
        elif users_subject.gender == "female":
            off_order_instructions_dict[instruction_query.off_order_place] = instruction_query.instruction_text_female
        else:
            off_order_instructions_dict[instruction_query.off_order_place] = instruction_query.instruction_text
    # edding an introduction to current phase with current errors (assuming its an Instruction page, otherwise nothing will be presented if not specified)
    if len(errors)>0:
        errors_introduction = []
        for instruction_query in off_order_instruction_queryset:
            if instruction_query.off_order_place == "onError":
                if users_subject.gender == "male":
                    errors_introduction.append(instruction_query.instruction_text_male)
                else:
                    errors_introduction.append(instruction_query.instruction_text_female)

        instructions_list = errors_introduction + instructions_list

    off_order_instruction_queryset = Instruction.objects.filter(str_phase__name="GeneralPhase")
    for instruction_query in off_order_instruction_queryset:
        if users_subject.gender == "male":
            off_order_instructions_dict[instruction_query.off_order_place] = instruction_query.instruction_text_male
        elif users_subject.gender == "female":
            off_order_instructions_dict[instruction_query.off_order_place] = instruction_query.instruction_text_female
        else:
            off_order_instructions_dict[instruction_query.off_order_place] = instruction_query.instruction_text

    return instructions_list, off_order_instructions_dict, pictures_paths

# creates a  BLANK Subject model instance and associtates it with ForeignKey to the authenticated user
def _create_subject(user):
    new_subject = Subject(experiment=Experiment.objects.get(name="IPA2"))
    new_subject.save()
    new_subject.is_subject = True
    new_subject.name = "Subject-"+user.usertosubjectipa2.subject_num
    new_subject.subject_session = EXPERIMENT_FIRST_SESSION[EXPERIMENT_NAME] # on creation subject session is one
    new_subject.context_group = Context.objects.get(name="neutral") # neutral = no context
    #new_subject.session_1_ps, new_subject.session_2_ps = _get_sessions_ps(new_subject.context_group)
    new_subject.current_phase = ExperimentPhase.objects.get(name="Consent phase")
    new_subject.subject_num = user.usertosubjectipa2.subject_num
    new_subject.profile_label_set = user.usertosubjectipa2.features_set
    new_subject.age = user.usertosubjectipa2.age
    new_subject.education = user.usertosubjectipa2.education
    new_subject.gender = user.usertosubjectipa2.gender
    new_subject.runningLocation = user.usertosubjectipa2.runningLocation
    new_subject.start_time = datetime.datetime.now()
    orders = ["A,C", "C,A"]
    new_subject.sets_order = orders[random.randint(0,1)]

    new_subject.save(force_update=True)
    user.save()
    return new_subject

# return the Subject instance associated with the authenticated user
def _get_user_subject(user):
    if _check_if_user_have_subject(user):
        subject = Subject.objects.get(subject_num=user.usertosubjectipa2.subject_num)
    else: # a need to create a subject..
        subject = _create_subject(user)
    return subject

# returns a boolean depending on whether user has an associated Subject instance
def _check_if_user_have_subject(user):
    context = ""
    if Subject.objects.filter(subject_num=user.usertosubjectipa2.subject_num).exists(): # check if encrypted number represent a valid pk in Subject
        return True
    return False

# returns a context dictionary withh all the profiles data ready for rendering (a sort od serialiser)
def _get_profiles_list_context(all_profiles,  label_set=None):
    if label_set == None:
         label_set="A"

    profiles_data = {}
    profiles_data["profiles_list"] = [] # This is the list the will be iterated through the experiment
    for profile in all_profiles:
        p_id = profile.id
        if profile.id in profiles_data.keys():
            p_id = str(profile.id)+"-d" # dubbled profile
        profiles_data[p_id] = {}
        profiles_data["profiles_list"].append(p_id)
        features_list = profile.featurevalue_set.all()[::1] # the [::1] converts the query set into a list
        if profile.is_subject:
            features_list = [feature for feature in features_list if feature.target_feature.label_set==label_set]

        profiles_data[p_id]["name"] = profile.name
        profiles_data[p_id]["is_subject"] = profile.is_subject
        profiles_data[p_id]["features"] = {}
        profiles_data[p_id]["features_order"] = []
        for f in features_list:
            f_name = f.target_feature.feature_name
            profiles_data[p_id]["features_order"].append(f_name)
            profiles_data[p_id]["features"][f_name] = {}
            profiles_data[p_id]["features"][f_name]["value"] = f.value
            profiles_data[p_id]["features"][f_name]["l"] = f.target_feature.left_end
            profiles_data[p_id]["features"][f_name]["r"] = f.target_feature.right_end
            profiles_data[p_id]["features"][f_name]["name_to_present"] = f.target_feature.presenting_name
        random.shuffle(profiles_data[p_id]["features_order"])

    random.shuffle(profiles_data["profiles_list"])
    return profiles_data

def get_profile_question_text(subject, fl):
    text = ""
    if subject.current_phase.name == "Get Max Similarity Profile":
        if subject.gender == "male":
            if fl.feature_name =="c3":
                text = fl.question_heb_max_min_ideal_male.format(subject.max_similarity_name, "{}")
            else:
                text = fl.question_heb_max_min_ideal_male.format(subject.max_similarity_name)
        else:
            if fl.feature_name =="c3":
                text = fl.question_heb_max_min_ideal_female.format(subject.max_similarity_name, "{}")
            else:
                text = fl.question_heb_max_min_ideal_female.format(subject.max_similarity_name)
    elif subject.current_phase.name == "Get Min Similarity Profile":
        if subject.gender == "male":
            if fl.feature_name =="c3":
                text = fl.question_heb_max_min_ideal_male.format(subject.min_similarity_name, "{}")
            else:
                text = fl.question_heb_max_min_ideal_male.format(subject.min_similarity_name)
        else:
            if fl.feature_name =="c3":
                text = fl.question_heb_max_min_ideal_female.format(subject.min_similarity_name, "{}")
            else:
                text = fl.question_heb_max_min_ideal_female.format(subject.min_similarity_name)
    elif subject.current_phase.name == "Get Ideal Profile":
        if subject.gender == "male":
            if fl.feature_name =="c3":
                text = fl.question_heb_max_min_ideal_male.format("העצמי האידאלי שלך", "{}")
            else:
                text = fl.question_heb_max_min_ideal_male.format("העצמי האידאלי שלך")
        else:
            if fl.feature_name =="c3":
                text = fl.question_heb_max_min_ideal_female.format("העצמי האידאלי שלך", "{}")
            else:
                text = fl.question_heb_max_min_ideal_female.format("העצמי האידאלי שלך")

    else: # get subject self profile
        if subject.gender == "male":
            text = fl.question_heb_male
        else:
            text = fl.question_heb_female
    return text

# Preparing context for the a new subject page
def _get_new_subject_profile_page_context(users_subject, set_num):
    if set_num ==1:
        label_set = users_subject.sets_order.split(",")[0]
    else:
        label_set = users_subject.sets_order.split(",")[1]

    features_list = []
    for fl in FeatureLabels.objects.filter(label_set=label_set).all():
        question_text = get_profile_question_text(users_subject, fl)
        features_list.append([fl.feature_name, fl.right_end, fl.left_end, question_text])
    random.shuffle(features_list)

    if users_subject.current_phase.name == "During Get Profile1":
        sham_list = []
        for sq in ShamQuestion.objects.all():
            question_text = get_profile_question_text(users_subject, sq)
            sham_list.append([sq.sham_name, sq.right_end, sq.left_end, question_text])
        features_list = sham_list + features_list

    return {"features_list" : json.dumps(features_list)}

# Builds a generic context that is used in all views (db-html-js context, not manipulated context)
def _get_context(form_phase, instructions_list, single_instruction_text, off_order_instructions, words_to_highlight, pictures_paths, n_trials, n_practice_trials, errors, subject_group):
    context = {
                "form_phase": form_phase,
                "instructions_list":  json.dumps(instructions_list),
                "off_order_instructions_dict": off_order_instructions,
                "single_instructions": single_instruction_text,
                "n_trials": n_trials,
                "n_practice_trials": n_practice_trials,
                "subject_group": subject_group,
                "errors": errors,
                "errorsJSON": json.dumps(errors),
                "pictures_paths": pictures_paths,
                "words_to_highlight": json.dumps(words_to_highlight),
                }
    return context

def _get_subject_profile(users_subject, label_set=None):
    if label_set==None:
        label_set = users_subject.profile_label_set

    user_profile = ProfileModel.objects.get(name = users_subject.name)
    user_profile_data = {"features": {}, "features_order": [], "name": user_profile.name, "is_subject": user_profile.is_subject}
    features_data = user_profile.featurevalue_set.all()[::1] # the [::1] converts the query set into a list
    features_data = [feature for feature in features_data if feature.target_feature.label_set==label_set]
    for feature in features_data:
        f_name = feature.target_feature.feature_name
        user_profile_data["features_order"].append(f_name)
        user_profile_data["features"][f_name] = {}
        user_profile_data["features"][f_name]["value"] = feature.value
        user_profile_data["features"][f_name]["l"] = feature.target_feature.left_end
        user_profile_data["features"][f_name]["r"] = feature.target_feature.right_end
        user_profile_data["features"][f_name]["name_to_present"] = feature.target_feature.presenting_name

    random.shuffle(user_profile_data["features_order"])
    return user_profile_data

def _get_feature_distance_dict(subject_profile, other_profile):
    distances_dict = {}
    for f_name in subject_profile["features"]:
        d = abs(subject_profile["features"][f_name]["value"] - other_profile["features"][f_name]["value"])
        distances_dict[f_name] = d
    return distances_dict

def _get_subject_other_similarity(model, sp, ap):
    difference = 0
    for f_name in sp["features"]:
        s_value = sp["features"][f_name]["value"] # subject profile
        a_value = ap["features"][f_name]["value"] # artificial profile
        w = model.featureweight_set.get(feature_label__feature_name=f_name).value
        difference += w*abs(s_value - a_value)/100
    similarity = 1-difference
    return similarity

def _get_min_similarity(model, subject_profile):
    similarity = 0
    ammount_of_features = len(subject_profile["features"])
    for f_name in subject_profile["features"]:
         value = subject_profile["features"][f_name]["value"]
         distance = (100-value if value<=50 else value)/100
         if len(model.featureweight_set.filter(feature_label__feature_name=f_name)) == 0:
             w = 1/ammount_of_features # In case current feaures set doesnt have an equivalent model
         else:
             w = model.featureweight_set.get(feature_label__feature_name=f_name).value
         similarity += w*distance
    return 1-similarity

def print_profile_debug(model, ap, sp):
    print(_get_subject_other_similarity(model, ap, sp))
    for feature in ap["features_order"]:
        print(feature + " - " + str(ap["features"][feature]["value"]))

def _generate_profile(users_subject, target_similarity, label_set, name_instance=""):
    sp = _get_subject_profile(users_subject, label_set) # subject profile
    model = SimilarityContextModel.objects.get(context__name=users_subject.context_group.name, label_set=label_set)
    min_s = _get_min_similarity(model, sp) # min possible similarity
    relative_similarity_level = (1-min_s)*target_similarity + min_s
    initial_profile = copy.deepcopy(sp)

    ap = create_artificial_profile_3(sp, target_similarity, relative_similarity_level, model, initial_profile, _get_subject_other_similarity)
    random.shuffle(ap["features_order"]) ## Maybe should be in the same order
    ap["is_subject"] = False
    ap_name = "Artificial-" + str(target_similarity) + "-" + name_instance + "-Subject-" + users_subject.subject_num
    ap["name"] = ap_name

    # save this profile
    ArtificialProfileModel.objects.filter(target_subject=users_subject, name=ap_name, profile_label_set=label_set).delete() # first_deleting an existing profile
    ap_instance = ArtificialProfileModel(is_artificial=True, target_subject=users_subject)
    ap_instance.name = ap_instance.get_name_pattern(str(target_similarity), name_instance)
    ap_instance.target_phase = users_subject.current_phase
    ap_instance.profile_label_set = label_set
    ap_instance.save()
    feaure_labels = FeatureLabels.objects.filter(label_set=label_set).values_list("feature_name", flat=True)
    for feature_name in feaure_labels:
        feature = FeatureLabels.objects.get(feature_name=feature_name)
        feature_value = ap["features"][feature_name]["value"]
        ap_feature = FeatureValue(target_profile=ap_instance, target_feature=feature, value=feature_value)
        ap_feature.save()
        ap_instance.save(force_update=True)

    return ap

def _get_list_from_query_set(qset):
    l = []
    for i in qset:
        l.append(i)
    return l

def _create_subject_artificials_for_this_phase(subject, label_set=None, practice_name="Practice", trials_name="Trials"):
    if label_set==None:
        label_set = subject.profile_label_set
    '''Generates subject artificial profiles for the current phase '''
    practice_similarities_levels = subject.current_phase.get_practice_trials_content()

    for slevel in practice_similarities_levels:
        _generate_profile(subject, slevel, label_set, name_instance=subject.current_phase.name+" - " + practice_name)

    similarities_levels = subject.current_phase.get_trials_content()
    for slevel in similarities_levels:
        _generate_profile(subject, slevel, label_set, name_instance=subject.current_phase.name+" - " + trials_name)

def get_dubbled_profiles_list(subject, trials):
    dubbled_profiles = []
    similarity_levels_to_dubble = subject.experiment.dubbled_artificials_list.split(", ")
    for profile in _get_list_from_query_set(trials):
        for slevle in similarity_levels_to_dubble:
            if slevle in profile.name:
                dubbled_profiles.append(profile)
    return dubbled_profiles

def _get_profile_list_for_profiles_presentation_phase(subject):
    _create_subject_artificials_for_this_phase(subject, label_set="A")
    _create_subject_artificials_for_this_phase(subject, label_set="C")

    regulars_A = ProfileModel.objects.filter(profile_label_set="A", is_artificial=False, is_subject=False, is_MinMax=False).all()
    regulars_C = ProfileModel.objects.filter(profile_label_set="C", is_artificial=False, is_subject=False, is_MinMax=False).all()

    # min_max = MinMaxProfileModel.objects.filter(profile_label_set=subject.profile_label_set,target_subject=subject).all()

    artificials_A = ArtificialProfileModel.objects.filter(profile_label_set="A",target_subject=subject, target_phase=subject.current_phase).all()
    artificials_C = ArtificialProfileModel.objects.filter(profile_label_set="C",target_subject=subject, target_phase=subject.current_phase).all()

    sp_model = ProfileModel.objects.filter(name=subject.name, is_artificial=False, is_subject=True, is_MinMax=False).all()

    practice_A = artificials_A.filter(name__contains='Practice')
    trials_A = artificials_A.filter(name__contains='Trials')

    practice_C = artificials_C.filter(name__contains='Practice')
    trials_C = artificials_C.filter(name__contains='Trials')

    all_A  = _get_list_from_query_set(regulars_A) + _get_list_from_query_set(trials_A) \
        + _get_list_from_query_set(sp_model) #+ get_dubbled_profiles_list(subject, trials_A)

    all_C  = _get_list_from_query_set(regulars_C) + _get_list_from_query_set(sp_model) + _get_list_from_query_set(trials_C) \
        #+ get_dubbled_profiles_list(subject, trials_C)

    practice_context_A = _get_profiles_list_context(practice_A) # _get_profiles_list_context also shuffles trials order
    practice_context_C = _get_profiles_list_context(practice_C) # _get_profiles_list_context also shuffles trials order

    regulars_min_max_trials_subject_A = _get_profiles_list_context(all_A, label_set="A") # _get_profiles_list_context also shuffles trials order
    regulars_min_max_trials_subject_C = _get_profiles_list_context(all_C,  label_set="C") # _get_profiles_list_context also shuffles trials order

    all_profiles_list_A = [] + regulars_min_max_trials_subject_A["profiles_list"]
    all_profiles_list_C = [] + regulars_min_max_trials_subject_C["profiles_list"]

    regulars_min_max_trials_subject_A.update(practice_context_A) # addint the profiles data
    regulars_min_max_trials_subject_C.update(practice_context_C) # addint the profiles data

    regulars_min_max_trials_subject_A["profiles_list"] = practice_context_A["profiles_list"] + all_profiles_list_A # putting practice profiles first
    regulars_min_max_trials_subject_C["profiles_list"] = practice_context_C["profiles_list"] + all_profiles_list_C # putting practice profiles first

    ids_to_profile_identifier_A, profile_identifier_to_ids_A = get_mapped_ids(regulars_min_max_trials_subject_A["profiles_list"])
    new_profiles_list_A = arrage_in_pairs(regulars_min_max_trials_subject_A["profiles_list"], ids_to_profile_identifier_A, profile_identifier_to_ids_A, "A")

    ids_to_profile_identifier_C, profile_identifier_to_ids_C = get_mapped_ids(regulars_min_max_trials_subject_C["profiles_list"])
    new_profiles_list_C = arrage_in_pairs(regulars_min_max_trials_subject_C["profiles_list"], ids_to_profile_identifier_C, profile_identifier_to_ids_C, "C")

    regulars_min_max_trials_subject_A["profiles_list"] = new_profiles_list_A
    regulars_min_max_trials_subject_C["profiles_list"] = new_profiles_list_C

    all_both = (regulars_min_max_trials_subject_A, regulars_min_max_trials_subject_C)
    return all_both

# arranges profiles list in pairs:
def arrage_in_pairs(profiles_list, ids_to_profile_identifier, profile_identifier_to_ids, label_set):
    pairs = [
                ["0.2", "0.8"],
                ["0.3", "0.7"],
                ["0.35", "0.65"],
                ["0.4", "0.6"],
                ["0.501", "0.5011"],
                ["0.9", "0.901"],
                ["0.301", "0.3011"],
                ["0.72", "1.0"],
            ]
    practice_pairs = [
                        ['0.7-p','0.2-p'],
                        ['0.32-p','0.62-p'],
                        ['0.41-p','0.51-p'],
                    ]

    new_profiles_list = []
    new_practice_profiles_list = []

    for pair in pairs:
        p_1 = profile_identifier_to_ids[pair[0]]
        p_2 = profile_identifier_to_ids[pair[1]]
        new_profiles_list.append([p_1, p_2])
    for pair in practice_pairs:
        p_1 = profile_identifier_to_ids[pair[0]]
        p_2 = profile_identifier_to_ids[pair[1]]
        new_practice_profiles_list.append([p_1, p_2])

    options = [o+1 for o in range(8)]
    ecos_list = []
    while len(options)>0:
        p1 = random.sample(options,1)[0]
        options.remove(p1)
        p2 = random.sample(options,1)[0]
        options.remove(p2)
        p1 = "Eco-{}-".format(label_set)+str(p1)
        p2 = "Eco-{}-".format(label_set)+str(p2)
        p1id = profile_identifier_to_ids[p1]
        p2id = profile_identifier_to_ids[p2]
        ecos_list.append([p1id,p2id])

    new_profiles_list = ecos_list + new_profiles_list
    random.shuffle(new_profiles_list)
    new_profiles_list = new_practice_profiles_list + new_profiles_list

    return new_profiles_list


# maps ids to identifiers and vise versa
def get_mapped_ids(profiles_list):
    ids_to_profile_identifier = {} # identifier = similarity level / Eco number / subject
    profile_identifier_to_ids = {} # identifier = similarity level / Eco number / subject
    for profile in profiles_list:
        p_object = ProfileModel.objects.get(id=profile)
        p_name = p_object.name
        if p_object.is_artificial:
            similarity_level = p_name.split("-")[1]
            if "Practice" in p_name:
                similarity_level = str(similarity_level)+"-p"
            ids_to_profile_identifier[profile] = similarity_level
            profile_identifier_to_ids[similarity_level] = profile
        elif p_object.is_subject:
            ids_to_profile_identifier[profile] = "subject"
            profile_identifier_to_ids["subject"] = profile
        else:
            ids_to_profile_identifier[profile] = p_name
            profile_identifier_to_ids[p_name] = profile
    return (ids_to_profile_identifier, profile_identifier_to_ids)

# Updates the generic context on specific phases
def _update_context_if_necessry(context, current_phase, users_subject):
    if current_phase == "During Get Profile1":
        context.update(_get_new_subject_profile_page_context(users_subject, 1))

    elif current_phase == "During Get Profile2":
        context.update(_get_new_subject_profile_page_context(users_subject, 2))

    elif current_phase =="Get Max Similarity Profile" or current_phase=="Get Min Similarity Profile" or current_phase=="Get Ideal Profile":
        context.update(_get_new_subject_profile_page_context(users_subject))

    elif current_phase == "Matrix tutorial":
        game = _get_game_data(users_subject)
        gameJSON = json.dumps(_get_game_dict(game))
        context.update({"game":game,
                        "gameJSON":gameJSON,
                        })
    elif current_phase == "During Profile Presentation":
        peofiles_A, peofiles_C = _get_profile_list_for_profiles_presentation_phase(users_subject)
        trials = len(peofiles_A["profiles_list"])-3
        games_types = ["shoot"]*int(trials/2) + ["help"]*int(trials/2)
        random.shuffle(games_types)
        games_types = ["help", "shoot", "help"] + games_types
        context.update({"task_profiles_A":json.dumps(peofiles_A)})
        context.update({"task_profiles_C":json.dumps(peofiles_C)})
        context.update({"gameTypes":json.dumps(games_types)})

    elif current_phase == "Identification Task":
        _create_subject_artificials_for_this_phase(users_subject,  label_set="A", practice_name="---", trials_name="SlowPhase")
        _create_subject_artificials_for_this_phase(users_subject,  label_set="C", practice_name="---", trials_name="SlowPhase")
        artificials_A = ArtificialProfileModel.objects.filter(profile_label_set="A",target_subject=users_subject, target_phase=users_subject.current_phase).all()
        artificials_A = artificials_A.filter(~Q(name__contains="No_One"))
        artificials_C = ArtificialProfileModel.objects.filter(profile_label_set="C",target_subject=users_subject, target_phase=users_subject.current_phase).all()
        artificials_C = artificials_C.filter(~Q(name__contains="No_One"))
        slow_phase_A = _get_list_from_query_set(artificials_A.filter(name__contains='SlowPhase'))
        slow_phase_C = _get_list_from_query_set(artificials_C.filter(name__contains='SlowPhase'))
        trials_context_A = _get_profiles_list_context(slow_phase_A)
        trials_context_C = _get_profiles_list_context(slow_phase_C)
        trials_context_A.update(trials_context_A) # addint the profiles data -- update deletes current profiles_list and replace it with those of practice_context
        trials_context_C.update(trials_context_C) # addint the profiles data -- update deletes current profiles_list and replace it with those of practice_context
        sp_A = _get_subject_profile(users_subject, label_set="A") # getting subject profile
        sp_C = _get_subject_profile(users_subject, label_set="C") # getting subject profile

        # none_of_the_above creation
        trials_nta_indexes = random.sample(range(len(trials_context_A["profiles_list"])), 4) # only on "A" so that both sets trials' lists will be on the same indexes
        similarity_levels = [0.4, 0.5, 0.6, 0.7]
        for i, trial in enumerate(trials_nta_indexes):
            _generate_profile(users_subject, similarity_levels[i], "A", name_instance=users_subject.current_phase.name+" - " + "SlowPhase-No_One-1")
            _generate_profile(users_subject, similarity_levels[i], "A", name_instance=users_subject.current_phase.name+" - " + "SlowPhase-No_One-2")
            _generate_profile(users_subject, similarity_levels[i], "C", name_instance=users_subject.current_phase.name+" - " + "SlowPhase-No_One-1")
            _generate_profile(users_subject, similarity_levels[i], "C", name_instance=users_subject.current_phase.name+" - " + "SlowPhase-No_One-2")
            trials_context_A["profiles_list"].insert(trial+i, "no_one")
            trials_context_C["profiles_list"].insert(trial+i, "no_one")
        no_one_profiles_A = ArtificialProfileModel.objects.filter(name__contains ="SlowPhase-No", profile_label_set="A", target_subject=users_subject)
        no_one_profiles_C = ArtificialProfileModel.objects.filter(name__contains ="SlowPhase-No", profile_label_set="C", target_subject=users_subject)
        no_one_profiles_context_A = _get_profiles_list_context(no_one_profiles_A)
        no_one_profiles_context_C = _get_profiles_list_context(no_one_profiles_C)
        no_one_pairs_indexes_A = []
        no_one_pairs_indexes_C = []
        for slevel in similarity_levels:
            p1, p2 = no_one_profiles_A.filter(name__contains = str(slevel))
            no_one_pairs_indexes_A.append([p1.id, p2.id])
            p1, p2 = no_one_profiles_C.filter(name__contains = str(slevel))
            no_one_pairs_indexes_C.append([p1.id, p2.id])

        total_trials_ammount = len(trials_context_A["profiles_list"])
        set_trials = ["A"]*int(total_trials_ammount/2) + ["C"]*int(total_trials_ammount/2)
        random.shuffle(set_trials)
        users_subject.trials_set += ','.join(set_trials) + ","
        users_subject.save()
        d2 = {"set_trials" : json.dumps(set_trials),
                "identification_task" : json.dumps({"subject_A": sp_A,
                                                "subject_C":sp_C,
                                                "artificials_A":trials_context_A,
                                                "artificials_C":trials_context_C,
                                                "no_one_pairs_indexes_A": no_one_pairs_indexes_A,
                                                "no_one_pairs_indexes_C": no_one_pairs_indexes_C,
                                                "no_one_profiles_A":no_one_profiles_context_A,
                                                "no_one_profiles_C":no_one_profiles_context_C,
                                                "no_one_trial_indexes": trials_nta_indexes
                                                })}
        context.update(d2)

    return context # if condition fails, context remain untouched

def _get_enriched_instructions_if_nesseccary(subject, phases_instructions, single_instruction, off_order_instructions):
    words_to_highlight = []
    if subject.current_phase.name == "Get Min Max Similarity":
        words_to_highlight = words_to_highlight + ["הדומה לך ביותר", "הכי פחות", "כדומה לך ביותר"]
    elif subject.current_phase.name == "Pre Get Max Profile":
        single_instruction = single_instruction.format(subject.max_similarity_name, subject.max_similarity_name)
        words_to_highlight = words_to_highlight+ [subject.max_similarity_name, "כדומה לך ביותר"]
        phases_instructions[0] = phases_instructions[0].format(subject.max_similarity_name, subject.max_similarity_name)
    elif subject.current_phase.name == "Pre Get Min Profile":
        single_instruction = single_instruction.format(subject.min_similarity_name, subject.min_similarity_name)
        words_to_highlight = words_to_highlight+ [subject.min_similarity_name,"כהכי פחות דומה לך"]
        phases_instructions[0] = phases_instructions[0].format(subject.min_similarity_name, subject.min_similarity_name)
    elif subject.current_phase.name == "Pre Get Profile":
        phases_instructions[0] = phases_instructions[0].format(off_order_instructions[subject.profile_label_set])
    elif subject.current_phase.name == "Matrix tutorial":
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

    return phases_instructions, single_instruction, off_order_instructions, words_to_highlight

def _get_n_trials_and_practice_trials(subject):
    trials = (subject.current_phase.n_trials, subject.current_phase.n_practice_trials)
    return trials

#####################################################################################################################################################################
# IPA-2 Unique Views:################################################################################################################################################
#####################################################################################################################################################################

# Returns one of the contexts
def _get_random_context():
    contexts = ["trade", "violence", "romantic","friendship"]
    return contexts[random.randint(0, len(contexts)-1)] # temporary - TODO: monitro with db maybe via the Experiment model

# Returns the current session ps
def _get_sessions_ps(context):
    rand_i = random.randint(0, 1) # temporary - TODO: monitro with db maybe via the Experiment model
    other_i =(rand_i - 1) * -1
    subjects_context = Context.objects.get(name=context)
    games = GameMatrix.objects.filter(context_group=subjects_context) # assuming only tow games Ps* per context
    pss = (games[rand_i].ps_threshold, games[other_i].ps_threshold)
    return pss

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

#####################################################################################################################################################################
## Experiment Views: ################################################################################################################################################
#####################################################################################################################################################################
def render_next_phase(request, users_subject):
    errors = [] # a place holder for errors
    if request.method == "POST":
        errors = forms_processor.process_form(users_subject.current_phase.name, request.POST)
        errors = [] if errors == None else errors # making sure errors are provided as list
        phases_data_saver.save_posted_data(users_subject.current_phase.name, request.POST, users_subject)
        if (len(errors) == 0) & (request.POST[form_phase] == users_subject.current_phase.name):
            # condition fails on errors or GET (user was sent from home page with a get method) or
            #in case of page refresh request.POST is previous phasewhile users_subject.current_phase.name moved forward
            _update_subject_phase(users_subject) # updates "users_subject.current_phase"
            if users_subject.current_phase.name == "End Screen":
                users_subject.update_subject_session_on_complete()
                sd = SubjectData()
                sd.save_subject_data(users_subject, ProfileModel, MinMaxProfileModel, ArtificialProfileModel)
        else: # in case of errorsJSON
            if users_subject.current_phase.name == "Identification Task":
                users_subject.n_identification_task_rounds += 1 # saving an occurance of mistkes in identification task
                users_subject.save()
            if users_subject.n_identification_task_rounds > users_subject.experiment.n_identification_rounds_allowed:
                users_subject.update_subject_session_on_complete()
                sd = SubjectData()
                sd.save_subject_data(users_subject, ProfileModel, MinMaxProfileModel, ArtificialProfileModel, partial_save=True)
                users_subject.current_phase = ExperimentPhase.objects.get(name="End Screen")
                users_subject.save()

            if users_subject.current_phase.name == "Identification Task": # on concent and demographics we want to stay in place and not go back
                _update_subject_phase(users_subject, direction=-1) # updates downwards "users_subject.current_phase"

    phases_instructions, off_order_instructions, pictures_paths = _get_phases_instructions(users_subject.current_phase.name, users_subject, errors)
    single_instruction = phases_instructions[0] if len(phases_instructions) == 1 else None
    n_trials, n_practice_trials = _get_n_trials_and_practice_trials(users_subject)
    phases_instructions, single_instruction, off_order_instructions, words_to_highlight = _get_enriched_instructions_if_nesseccary(users_subject, phases_instructions, single_instruction, off_order_instructions)
    context_to_send = _get_context(users_subject.current_phase.name, phases_instructions, single_instruction, off_order_instructions, words_to_highlight, pictures_paths, n_trials, n_practice_trials, errors, users_subject.profile_label_set)
    context_to_send = _update_context_if_necessry(context_to_send, users_subject.current_phase.name, users_subject)

    if request.method == "GET" and users_subject.current_phase.name == "End Screen":
        users_subject.update_subject_session_on_complete()
        lpartial_save=False
        if users_subject.n_identification_task_rounds > users_subject.experiment.n_identification_rounds_allowed:
            lpartial_save=True
        sd = SubjectData()
        sd.save_subject_data(users_subject, ProfileModel, MinMaxProfileModel, ArtificialProfileModel, partial_save=lpartial_save)

    return render(request, 'ipa_2/{}.html'.format(phase_to_html_page[users_subject.current_phase.name]), context_to_send)

# A general function that serves as phase decider
def get_phase_page(request):
    if  request.user.is_anonymous:
        return redirect(reverse("signin_ipa2"))
    else:
        users_subject = _get_user_subject(request.user)
        # TODO: Make sure user is authenticated.. subject is ready --> maybe already take care for
        # TODO: Make sure subject did not already finished this expperiment
        # TODO: maybe make user subject creation be mediated by a mail an a manual connection (no in DB)
        return render_next_phase(request, users_subject)

def get_data_page(request):
    from distutils.dir_util import copy_tree

    data_path = "ipa_2/static/ipa_2/data/"
    files = os.listdir(data_path)
    paths = []
    df_paths = []

    for file in files:
        paths.append(os.path.join("ipa_2/data/", file))
        df_paths.append(os.path.join(data_path, file))

    paths_files = zip(paths, files)

    df_all = get_single_df_all_data(data_path)
    df_all.to_excel(os.path.join(data_path, "all_data.xlsx"), index=False)


    to_dir = os.path.join("static", "ipa_2", "data")
    to_dir_files = os.listdir(to_dir)
    to_dir_files = [file.split("/")[-1] for file in to_dir_files]
    df_paths = [added_file for added_file in df_paths if not added_file.split("/")[-1] in to_dir_files]
    df_paths.append(all_data_path)
    from_dir = data_path

    copy_tree(from_dir, to_dir)

    exp = Experiment.objects.get(name="IPA2")
    bounuses = get_bonuses_dict(exp.subject_bonuses)
    for df in df_paths:
        if df.endswith(".xlsx") and "Subject" in df:
            subject_num = df.split("-")[1]
            if not subject_num in bounuses.keys():
                ad = AnalyzeData(df)
                bounuses[subject_num] = ad.get_subject_bonus()
    bounuses_string = get_string_from_bonuses_dict(bounuses)
    exp.subject_bonuses = bounuses_string
    exp.save()
    return render(request, 'ipa_2/data.html', {"paths_files": paths_files, "bounuses": json.dumps(bounuses)})

def get_bonuses_dict(bounuses_string):
    bounuses_string = bounuses_string.split(",")
    bonuses_dict = {}
    for kvp in bounuses_string:
        if kvp != "":
            k,v = kvp.split("-")
            bonuses_dict[k] = v
    return bonuses_dict

def get_string_from_bonuses_dict(bonuses_dict):
    bounuses_string = ""
    for k,v in bonuses_dict.items():
        bounuses_string = bounuses_string + str(k) + "-" + str(v) + ","
    return bounuses_string

def save_try(request):
    users_subject = _get_user_subject(request.user)
    sd = SubjectData()
    sd.save_subject_data(users_subject, ProfileModel, MinMaxProfileModel, ArtificialProfileModel)
    return render(request, 'ipa_2/endPage.html')

def get_single_df_all_data(data_dir):
    files = os.listdir(r''+data_dir)

    all_data_file_path = os.path.join(data_dir,"all_data.xlsx")
    existing_subjects = []
    if not os.path.exists(all_data_file_path):
        all_data = pd.DataFrame()
    else:
        all_data = pd.read_excel(all_data_file_path)
        existing_subjects = all_data.subject_num.unique().tolist()

    for file in files:
        if file.endswith(".xlsx") and file != "all_data.xlsx":
            subject_num = int(file.split("-")[1])
            if not subject_num in existing_subjects:
                df = pd.read_excel(os.path.join(r''+data_dir,file))
                subject_group = df.subject_group.unique()[0]
                for i in range(len(COL_NAMES_BY_GROUP[subject_group])):
                    subject_feature = COL_NAMES_BY_GROUP[subject_group][i]
                    profile_feature = PROFILE_COL_NAMES_BY_GROUP[subject_group][i]
                    df["Feature-"+str(i+1)] = (100 - (abs(df[subject_feature]-df[profile_feature])))/100
                all_data = all_data.append(df)
    return all_data

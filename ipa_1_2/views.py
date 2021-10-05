from django.db.models import Q
from django.shortcuts import render, redirect, reverse, get_object_or_404
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

from .myUtils.FormsProcessing import FormsProcessor, PhasesDataSaver
from .myUtils.ArticialProfile import create_artificial_profile_3
from .myUtils.SubjectData import SubjectData

phase_to_html_page = {
                        "Consent phase":                "Index",
                        "Pre Task":                     "instruction",
                        "Get Min Max Similarity":       "MinMaxSimilariy",
                        "Pre Get Profile":              "instruction",
                        "During Get Profile":           "GetSubject/getSubjectProfile",
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
                        "Get Ideal Profile":   "GetSubject/getSubjectProfile",
                        "End Screen":                   "endPage",
                        "Session End":                   "endPage",
                    }

form_phase = "form_phase"

forms_processor = FormsProcessor(GameMatrix)
phases_data_saver = PhasesDataSaver(FeatureLabels, FeatureValue, MinMaxProfileModel)

EXPERIMENT_NAME = "ipa_1_2"
EXPERIMENT_FIRST_SESSION = {"ipa_1_2" : 2, "SGS1": 1}
## Assistant functions: ###############################################################################################################################################
# saves subject model with the new phase
def _update_subject_phase(subject, direction=None):
    subject_updated_phase = _get_next_phase(subject, direction=direction)
    subject.current_phase = subject_updated_phase
    subject.save()

 # return a query set of all phases-model instances associated with this subject's experiment
def _get_all_subject_phases(subject):
    return subject.experiment.experimentphase_set.all()

# returns the name of next phase of this subject
def _get_next_phase(subject, direction=None):
    if direction==None:
        direction=1
    phases = ExperimentPhase.objects.all()
    if subject.current_phase.name != "Session End":
        # ipdb.set_trace()
        next_phase = phases.get(phase_place=subject.current_phase.phase_place+(direction*1))
        return next_phase
    else: # upon ending a session
        return subject.current_phase

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
                pictures_paths.append(r'/static/ipa_1_2/media/images/' + pic_name)



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
    return instructions_list, off_order_instructions_dict, pictures_paths

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

# creates a  BLANK Subject model instance and associtates it with ForeignKey to the authenticated user
def _create_subject(user):
    new_subject = Subject(experiment=Experiment.objects.get(name="IPA1.2"))
    new_subject.save()
    new_subject.is_subject = True
    new_subject.name = "Subject-"+user.usertosubject.subject_num
    new_subject.subject_session = EXPERIMENT_FIRST_SESSION[EXPERIMENT_NAME] # on creation subject session is one
    new_subject.context_group = "neutral" # neutral = no context
    #new_subject.session_1_ps, new_subject.session_2_ps = _get_sessions_ps(new_subject.context_group)
    new_subject.current_phase = ExperimentPhase.objects.get(name="Consent phase")
    new_subject.subject_num = user.usertosubject.subject_num
    new_subject.profile_label_set = user.usertosubject.features_set
    new_subject.age = user.usertosubject.age
    new_subject.education = user.usertosubject.education
    new_subject.gender = user.usertosubject.gender
    new_subject.start_time = pytz.timezone("Israel").localize(datetime.datetime.now())
    new_subject.save(force_update=True)
    user.save()
    return new_subject

# return the Subject instance associated with the authenticated user
def _get_user_subject(user):
    if _check_if_user_have_subject(user):
        subject = Subject.objects.get(subject_num=user.usertosubject.subject_num)
    else: # a need to create a subject..
        subject = _create_subject(user)
    return subject

# returns a boolean depending on whether user has an associated Subject instance
def _check_if_user_have_subject(user):
    context = ""
    ###################
    if Subject.objects.filter(subject_num=user.usertosubject.subject_num).exists(): # check if encrypted number represent a valid pk in Subject
        return True
    return False

# returns a context dictionary withh all the profiles data ready for rendering (a sort od serialiser)
def _get_profiles_list_context(all_profiles):
    profiles_data = {}
    profiles_data["profiles_list"] = [] # This is the list the will be iterated through the experiment
    for profile in all_profiles:
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
            profiles_data[profile.id]["features"][f_name]["name_to_present"] = f.target_feature.presenting_name
        random.shuffle(profiles_data[profile.id]["features_order"])

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
def _get_new_subject_profile_page_context(users_subject):
    features_list = []
    for fl in FeatureLabels.objects.filter(label_set=users_subject.profile_label_set).all():
        question_text = get_profile_question_text(users_subject, fl)
        features_list.append([fl.feature_name, fl.right_end, fl.left_end, question_text])
    random.shuffle(features_list)

    if users_subject.current_phase.name == "During Get Profile":
        sham_list = []
        for sq in ShamQuestion.objects.all():
            question_text = get_profile_question_text(users_subject, sq)
            sham_list.append([sq.sham_name, sq.right_end, sq.left_end, question_text])
        features_list = sham_list + features_list

    return {"features_list" : json.dumps(features_list)}

# Builds a generic context that is used in all views (db-html-js context, not manipulated context)
def _get_context(form_phase, instructions_list, single_instruction_text, off_order_instructions, words_to_highlight, pictures_paths, n_trials, n_practice_trials, errors):
    context = {
                "form_phase": form_phase,
                "instructions_list":  json.dumps(instructions_list),
                "off_order_instructions_dict": off_order_instructions,
                "single_instructions": single_instruction_text,
                "n_trials": n_trials,
                "n_practice_trials": n_practice_trials,
                "errors": errors,
                "errorsJSON": json.dumps(errors),
                "pictures_paths": pictures_paths,
                "words_to_highlight": json.dumps(words_to_highlight),
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

def _generate_profile(users_subject, target_similarity, name_instance=""):
    sp = _get_subject_profile(users_subject) # subject profile
    model = SimilarityContextModel.objects.get(context__name=users_subject.context_group, label_set=users_subject.profile_label_set)
    min_s = _get_min_similarity(model, sp) # min possible similarity
    relative_similarity_level = (1-min_s)*target_similarity + min_s
    initial_profile = copy.deepcopy(sp)

    ap = create_artificial_profile_3(sp, target_similarity, relative_similarity_level, model, initial_profile, _get_subject_other_similarity)
    random.shuffle(ap["features_order"]) ## Maybe should be in the same order
    ap["is_subject"] = False
    ap_name = "Artificial-" + str(target_similarity) + "-" + name_instance + "-Subject-" + users_subject.subject_num
    ap["name"] = ap_name

    # save this profile
    ArtificialProfileModel.objects.filter(target_subject=users_subject, name=ap_name).delete() # first_deleting an existing profile
    ap_instance = ArtificialProfileModel(is_artificial=True, target_subject=users_subject)
    ap_instance.name = ap_instance.get_name_pattern(str(target_similarity), name_instance)
    ap_instance.target_phase = users_subject.current_phase
    ap_instance.profile_label_set = users_subject.profile_label_set
    ap_instance.save()
    feaure_labels = FeatureLabels.objects.filter(label_set=users_subject.profile_label_set).values_list("feature_name", flat=True)
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

def _create_subject_artificials_for_this_phase(subject, practice_name="Practice", trials_name="Trials"):
    '''Generates subject artificial profiles for the current phase '''
    practice_similarities_levels = subject.current_phase.get_practice_trials_content()

    for slevel in practice_similarities_levels:
        _generate_profile(subject, slevel, name_instance=subject.current_phase.name+" - " + practice_name)

    similarities_levels = subject.current_phase.get_trials_content()
    for slevel in similarities_levels:
        _generate_profile(subject, slevel, name_instance=subject.current_phase.name+" - " + trials_name)


def _get_profile_list_for_profiles_presentation_phase(subject):
    _create_subject_artificials_for_this_phase(subject)
    regulars = ProfileModel.objects.filter(profile_label_set=subject.profile_label_set, is_artificial=False, is_subject=False, is_MinMax=False).all()
    min_max = MinMaxProfileModel.objects.filter(profile_label_set=subject.profile_label_set,target_subject=subject).all()
    artificials = ArtificialProfileModel.objects.filter(profile_label_set=subject.profile_label_set,target_subject=subject, target_phase=subject.current_phase).all()
    sp_model = ProfileModel.objects.filter(name=subject.name, profile_label_set=subject.profile_label_set, is_artificial=False, is_subject=True, is_MinMax=False).all()
    practice = artificials.filter(name__contains='Practice')
    trials = artificials.filter(name__contains='Trials')

    NUMBER_OF_DUBLICATED_ARTICIAL_PROFILES = 4
    all  = _get_list_from_query_set(min_max) + _get_list_from_query_set(regulars) + _get_list_from_query_set(sp_model) \
     + _get_list_from_query_set(trials) + random.sample(_get_list_from_query_set(trials), NUMBER_OF_DUBLICATED_ARTICIAL_PROFILES)

    practice_context = _get_profiles_list_context(practice) # _get_profiles_list_context also shuffles trials order
    regulars_min_max_trials_subject = _get_profiles_list_context(all) # _get_profiles_list_context also shuffles trials order
    all_profiles_list = [] + regulars_min_max_trials_subject["profiles_list"]
    regulars_min_max_trials_subject.update(practice_context) # addint the profiles data
    regulars_min_max_trials_subject["profiles_list"] = practice_context["profiles_list"] + all_profiles_list # putting practice profiles first
    regulars_min_max_trials_subject["profiles_list"] = regulars_min_max_trials_subject["profiles_list"]
    return regulars_min_max_trials_subject

# Updates the generic context on specific phases
def _update_context_if_necessry(context, current_phase, users_subject):
    if current_phase == "During Get Profile":
        context.update(_get_new_subject_profile_page_context(users_subject))

    elif current_phase =="Get Max Similarity Profile" or current_phase=="Get Min Similarity Profile" or current_phase=="Get Ideal Profile":
        context.update(_get_new_subject_profile_page_context(users_subject))

    elif current_phase == "Matrix tutorial":
        game = _get_game_data(users_subject)
        gameJSON = json.dumps(_get_game_dict(game))
        context.update({"game":game,
                        "gameJSON":gameJSON,
                        })
    elif current_phase == "During Profile Presentation":
        peofiles = _get_profile_list_for_profiles_presentation_phase(users_subject)
        context.update({"context":json.dumps(peofiles)})
        context.update({"maxValue":users_subject.max_similarity_value,
                        "maxName": json.dumps(users_subject.max_similarity_name),
                        "minValue":users_subject.min_similarity_value,
                        "minName": json.dumps(users_subject.min_similarity_name),
                        })
    elif current_phase == "Identification Task":
        _create_subject_artificials_for_this_phase(users_subject, practice_name="---", trials_name="SlowPhase")
        artificials = ArtificialProfileModel.objects.filter(profile_label_set=users_subject.profile_label_set,target_subject=users_subject, target_phase=users_subject.current_phase).all()
        artificials = artificials.filter(~Q(name__contains="No_One"))
        slow_phase = _get_list_from_query_set(artificials.filter(name__contains='SlowPhase'))
        trials_context = _get_profiles_list_context(slow_phase)
        trials_context.update(trials_context) # addint the profiles data -- update deletes current profiles_list and replace it with those of practice_context
        sp = _get_subject_profile(users_subject) # getting subject profile

        # none_of_the_above creation
        trials_nta_indexes = random.sample(range(len(trials_context["profiles_list"])), 4)
        similarity_levels = [0.4, 0.5, 0.6, 0.7]
        for i, trial in enumerate(trials_nta_indexes):
            _generate_profile(users_subject, similarity_levels[i], name_instance=users_subject.current_phase.name+" - " + "SlowPhase-No_One-1")
            _generate_profile(users_subject, similarity_levels[i], name_instance=users_subject.current_phase.name+" - " + "SlowPhase-No_One-2")
            trials_context["profiles_list"].insert(trial+i, "no_one")
        no_one_profiles = ArtificialProfileModel.objects.filter(name__contains ="SlowPhase-No", target_subject=users_subject)
        no_one_profiles_context = _get_profiles_list_context(no_one_profiles)
        no_one_pairs_indexes = []
        for slevel in similarity_levels:
            p1, p2 = no_one_profiles.filter(name__contains = str(slevel))
            no_one_pairs_indexes.append([p1.id, p2.id])
        d2 = {"identification_task" : json.dumps({"subject": sp,
                                                "artificials":trials_context,
                                                "no_one_pairs_indexes": no_one_pairs_indexes,
                                                "no_one_profiles":no_one_profiles_context,
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

def _get_n_trials_and_practice_trials(subject):
    trials = (subject.current_phase.n_trials, subject.current_phase.n_practice_trials)
    return trials







## Experiment Views: ################################################################################################################################################
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
                return render(request, 'ipa_1_2/endPage.html')
        else: # in case of errorsJSON
            _update_subject_phase(users_subject, direction=-1) # updates downwards "users_subject.current_phase"
    phases_instructions, off_order_instructions, pictures_paths = _get_phases_instructions(users_subject.current_phase.name, users_subject, errors)
    single_instruction = phases_instructions[0] if len(phases_instructions) == 1 else None
    n_trials, n_practice_trials = _get_n_trials_and_practice_trials(users_subject)
    phases_instructions, single_instruction, off_order_instructions, words_to_highlight = _get_enriched_instructions_if_nesseccary(users_subject, phases_instructions, single_instruction, off_order_instructions)
    context_to_send = _get_context(users_subject.current_phase.name, phases_instructions, single_instruction, off_order_instructions, words_to_highlight, pictures_paths, n_trials, n_practice_trials, errors)
    context_to_send = _update_context_if_necessry(context_to_send, users_subject.current_phase.name, users_subject)
    return render(request, 'ipa_1_2/{}.html'.format(phase_to_html_page[users_subject.current_phase.name]), context_to_send)

# A general function that serves as phase decider
def get_phase_page(request):
    users_subject = _get_user_subject(request.user)
    # TODO: Make sure user is authenticated.. subject is ready --> maybe already take care for
    # TODO: Make sure subject did not already finished this expperiment
    # TODO: maybe make user subject creation be mediated by a mail an a manual connection (no in DB)
    return render_next_phase(request, users_subject)

def get_data_page(request):
    data_path = "ipa_1_2/static/ipa_1_2/data/"
    files = os.listdir(data_path)
    paths = []
    for file in files:
        paths.append(os.path.join("ipa_1_2/data/", file))
    paths_files = zip(paths, files)
    return render(request, 'ipa_1_2/data.html', {"paths_files": paths_files})

def save_try(request):
    users_subject = _get_user_subject(request.user)
    sd = SubjectData()
    sd.save_subject_data(users_subject, ProfileModel, MinMaxProfileModel, ArtificialProfileModel)
    return render(request, 'ipa_1_2/endPage.html')



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
def polls_detail(request, poll_id, some):
    pass
    #ipdb.set_trace()

import ipdb
import random

def _get_bouderies(sp_value, ap_value, direction):
    ''' ap = articial profile
        sp = subject profile'''
    if direction == "towards":
        if ap_value < sp_value:
            return sp_value - ap_value
        elif ap_value > sp_value:
            return ap_value - sp_value
        elif ap_value == sp_value:
            return 0
    elif direction == "away":
        if ap_value < sp_value:
            return ap_value
        elif ap_value > sp_value:
            return 100 - ap_value

def _create_fake_prfile(num, subject_profile):
    for feature in subject_profile["features"].keys():
        subject_profile["features"][feature]["value"] = num
    return subject_profile

def _create_profile_at_realtive_similarity_same_feature_pattern(subject_profile, artificial_profile, target_similarity, model):
    for feature in subject_profile["features"].keys():
        subject_feature_value = subject_profile["features"][feature]["value"]
        profile_feature_value = subject_feature_value*target_similarity
        if subject_feature_value < 50:
            profile_feature_value = 100 - (100 - subject_feature_value) * (target_similarity)

        # at random cases, we change the location of the profile value to be above or below subject value if possible
        if random.randint(0,1) == 1:
            if profile_feature_value > subject_feature_value:
                d = profile_feature_value-subject_feature_value
                if d <= subject_feature_value:
                    profile_feature_value = subject_feature_value-d

            elif profile_feature_value < subject_feature_value:
                d = subject_feature_value-profile_feature_value
                if d <= 100-subject_feature_value:
                    profile_feature_value = subject_feature_value+d

        artificial_profile["features"][feature]["value"] = profile_feature_value
    return artificial_profile

def _get_two_random_features(feature_names):
    features_indexes = list(range(len(feature_names)-1))
    random.shuffle(features_indexes)
    feature_1 = feature_names[features_indexes[0]]
    feature_2 = feature_names[features_indexes[1]]
    return feature_1, feature_2

def create_artificial_profile_3(subject_profile, target_similarity, relative_similarity_level, model, artificial_profile, get_simialrity_function):
    # for development checks purpose: ########################
    # target_similarity = 0
    # subject_profile = _create_fake_prfile(50, subject_profile)
    # end development ########################################

    similarity = get_simialrity_function(model, subject_profile, artificial_profile)
    artificial_profile = _create_profile_at_realtive_similarity_same_feature_pattern(subject_profile, artificial_profile, target_similarity, model)
    similarity2 = get_simialrity_function(model, subject_profile, artificial_profile)
    # print(similarity2, relative_similarity_level, target_similarity)
    sampled = []

    feature_names = list(artificial_profile["features"].keys())
    feature_1, feature_2 = _get_two_random_features(feature_names)
    sampled = sampled + [feature_1, feature_2]

    f1_can_towards = _get_bouderies(subject_profile["features"][feature_1]["value"], artificial_profile["features"][feature_1]["value"], "towards")
    f1_can_away = _get_bouderies(subject_profile["features"][feature_1]["value"], artificial_profile["features"][feature_1]["value"], "away")
    f2_can_towards = _get_bouderies(subject_profile["features"][feature_2]["value"], artificial_profile["features"][feature_2]["value"], "towards")
    f2_can_away = _get_bouderies(subject_profile["features"][feature_2]["value"], artificial_profile["features"][feature_2]["value"], "away")

    # ipdb.set_trace()

    return artificial_profile

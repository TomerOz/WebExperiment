import os
import ipdb
import pandas as pd

class SubjectData(object):

    def debug_dict(self, data_dict):
        for k in data_dict.keys():
            print(k +"-" +  str(len(data_dict[k])))

    def save_subject_data(self, subject, ProfileModel, MinMaxProfileModel, ArtificialProfileModel):
        CURRENT_APP_NAME = 'ipa_1_2'
        path_to_empty_session_df = os.path.join(CURRENT_APP_NAME,"myUtils","empty_session_df.xlsx")
        self.empty_session_df = pd.read_excel(path_to_empty_session_df)

        # Creating subject dictionary with columns corresopnding to the empty session df:
        features = pd.read_excel(os.path.join(CURRENT_APP_NAME,"myUtils","features.xlsx")).feature.values
        self.subject_data_dictionary = {}
        for col in self.empty_session_df.columns:
            self.subject_data_dictionary.setdefault(col, [])

        subject_features_dictionary = subject.get_features_dict()
        self.meta_profiles = [subject] + self._get_list_from_query_set(MinMaxProfileModel.objects.filter(target_subject=subject))
        self.add_trials(subject, ProfileModel)
        self.debug_dict(self.subject_data_dictionary)
        ipdb.set_trace()

        subject_df = pd.DataFrame(self.subject_data_dictionary)
        data_path = "ipa_1_2/static/ipa_1_2/data/"
        path = os.path.join(data_path, "Subject-{}-Data.xlsx".format(str(subject.subject_num)))
        subject_df.to_excel(path, index=False)


    def _get_list_from_query_set(self, qset):
        l = []
        for i in qset:
            l.append(i)
        return l

    def _add_meta_data(self, subject, task_name, responses):
        subject.start_time = subject.start_time.replace(tzinfo=None)
        subject.end_time = subject.end_time.replace(tzinfo=None)
        for n in range(len(responses)):
            trial_num = n+1
            self.subject_data_dictionary["trial_num"].append(trial_num)
            self.subject_data_dictionary["trial_task"].append(task_name)
            self.subject_data_dictionary["subject_num"].append(subject.subject_num)
            self.subject_data_dictionary["gender"].append(subject.gender)
            self.subject_data_dictionary["age"].append(subject.age)
            self.subject_data_dictionary["max_value"].append(subject.max_similarity_value)
            self.subject_data_dictionary["min_value"].append(subject.min_similarity_value)
            self.subject_data_dictionary["max_name"].append(subject.max_similarity_name)
            self.subject_data_dictionary["min_name"].append(subject.min_similarity_name)
            self.subject_data_dictionary["subject_group"].append(subject.profile_label_set)
            self.subject_data_dictionary["session_num"].append(subject.subject_session)
            self.subject_data_dictionary["experiment"].append(subject.experiment.name)
            self.subject_data_dictionary["start_time"].append(subject.start_time)
            self.subject_data_dictionary["end_time"].append(subject.end_time)
            self.subject_data_dictionary["experiment_duration"].append((subject.end_time-subject.start_time).seconds/60)
            self.subject_data_dictionary["education"].append(subject.education)

    def trials_to_list(self, data, seperator=",", initial="-", end=","):
        data1 = data[len(initial):len(data)-len(end)]
        data2 = data1.split(seperator)
        return data2


    def add_trials(self, subject, ProfileModel):
        # identification task responses:
        identification_response = self.trials_to_list(subject.subject_reported_sides) # reponse
        identification_rts = self.trials_to_list(subject.identification_rts) # rt
        identification_p_name = self.trials_to_list(subject.identification_profiles) # profile name
        identification_info = self.trials_to_list(subject.subject_profile_sides) # info
        self.subject_data_dictionary["response_value"] = self.subject_data_dictionary["response_value"] + identification_response
        self.subject_data_dictionary["response_time"] = self.subject_data_dictionary["response_time"] + identification_rts
        self.subject_data_dictionary["trial_profile"] = self.subject_data_dictionary["trial_profile"] + identification_p_name
        self.subject_data_dictionary["trial_features_order"] = self.subject_data_dictionary["trial_features_order"] + [" "]*len(identification_response) # not relevant to this phase
        self.subject_data_dictionary["response_time_profiles"] = self.subject_data_dictionary["response_time_profiles"] + [" "]*len(identification_response) # not relevant to this phase
        self.subject_data_dictionary["response_time_features"] = self.subject_data_dictionary["response_time_features"] + [" "]*len(identification_response) # not relevant to this phase
        self._add_meta_data(subject, "identification", identification_response)

        # profiles responses
        profiles_response = self.trials_to_list(subject.trials_responses_list) # respons
        features_rts = self.trials_to_list(subject.feature_response_times, seperator="-**NextProfile**-", end="-**NextProfile**-") # rt
        profiles_rts = self.trials_to_list(subject.profiles_response_times, seperator=",", end="") # rt
        profiles_p_name = self.trials_to_list(subject.trials_string_list) # profile name
        features_order = self.trials_to_list(subject.trial_features_order, seperator="-**NextProfile**-", end="-**NextProfile**-") # info

        self.subject_data_dictionary["response_value"] = self.subject_data_dictionary["response_value"] + profiles_response
        self.subject_data_dictionary["response_time_profiles"] = self.subject_data_dictionary["response_time_profiles"] + profiles_rts
        self.subject_data_dictionary["response_time_features"] = self.subject_data_dictionary["response_time_features"] + features_rts
        self.subject_data_dictionary["trial_profile"] = self.subject_data_dictionary["trial_profile"] + profiles_p_name
        self.subject_data_dictionary["trial_features_order"] = self.subject_data_dictionary["trial_features_order"] + features_order
        self.subject_data_dictionary["response_time"] = self.subject_data_dictionary["response_time"] + [" "]*len(profiles_response) # not relevant to this phase
        self._add_meta_data(subject, "profiles", profiles_response)

        for profile_name in self.subject_data_dictionary["trial_profile"]:
            profile = ProfileModel.objects.get(name=profile_name)
            self.add_profile_features(profile, "profile_")
            for meta_profile in self.meta_profiles:
                prefix = self.get_profile_prefix(meta_profile)
                self.add_profile_features(meta_profile, prefix)

        for key in self.subject_data_dictionary:
            if len(self.subject_data_dictionary[key]) == 0:
                self.subject_data_dictionary[key] = [" "]*len(self.subject_data_dictionary["trial_profile"])

    def get_profile_prefix(self, profile):
        prefix = ""
        if profile.is_subject:
            prefix = "self_"
        elif profile.is_MinMax:
            name = profile.name.split("-")[0]
            if name == "Min":
                prefix = "min_"
            elif name == "Max":
                prefix = "max_"
            elif name == "Ideal":
                prefix = "ideal_"
        else: "profile_"

        return prefix

    def add_profile_features(self, profile, prefix):
        # features prefices:
        profile_features = profile.get_features_dict()
        for f in profile_features:
            subject_data_key = prefix+f
            self.subject_data_dictionary[subject_data_key].append(profile_features[f])
        # features names:
        '''
                "way_of_speech"
                "socio_economic"
                "ethnicity_skin_color"
                "personality"
                "dress_propeties"
                "political_affiliation"
                "hobbies"
                "body_size"
                "intelligence"
                "goodness"
                "age"
                "happiness"
                "normality"
                "appearnce"
                "interest"
                "sainity"
                "importance"
                "amazing"
                "c1"
                "c2"
                "c3"
                "c4"
                "c5"
                "c6"
                "c7"
                "c8"
                "c9"

        {
            "subject_num":[],
            "start_time":[],
            "end_time":[],
            "experiment_duration":[],
            "gender":[],
            "age":[],
            "education":[],
            "min_name":[],
            "min_value":[],
            "max_name":[],
            "max_value":[],
            "response_value":[],
            "response_time":[],
            "trial_num":[],
            "trial_profile":[],
            "profile_info(sides_or_description)":[],
            "subject_group":[],

            "self_way_of_speech":[],
            "self_socio_economic":[],
            "self_ethnicity_skin_color":[],
            "self_personality":[],
            "self_dress_propeties":[],
            "self_political_affiliation":[],
            "self_hobbies":[],
            "self_body_size":[],
            "self_intelligence":[],
            "self_goodness":[],
            "self_age":[],
            "self_happiness":[],
            "self_normality":[],
            "self_appearnce":[],
            "self_interest":[],
            "self_sainity":[],
            "self_importance":[],
            "self_amazing":[],
            "self_c1":[],
            "self_c2":[],
            "self_c3":[],
            "self_c4":[],
            "self_c5":[],
            "self_c6":[],
            "self_c7":[],
            "self_c8":[],
            "self_c9":[],
            "min_way_of_speech":[],
            "min_socio_economic":[],
            "min_ethnicity_skin_color":[],
            "min_personality":[],
            "min_dress_propeties":[],
            "min_political_affiliation":[],
            "min_hobbies":[],
            "min_body_size":[],
            "min_intelligence":[],
            "min_goodness":[],
            "min_age":[],
            "min_happiness":[],
            "min_normality":[],
            "min_appearnce":[],
            "min_interest":[],
            "min_sainity":[],
            "min_importance":[],
            "min_amazing":[],
            "min_c1":[],
            "min_c2":[],
            "min_c3":[],
            "min_c4":[],
            "min_c5":[],
            "min_c6":[],
            "min_c7":[],
            "min_c8":[],
            "min_c9":[],
            "max_way_of_speech":[],
            "max_socio_economic":[],
            "max_ethnicity_skin_color":[],
            "max_personality":[],
            "max_dress_propeties":[],
            "max_political_affiliation":[],
            "max_hobbies":[],
            "max_body_size":[],
            "max_intelligence":[],
            "max_goodness":[],
            "max_age":[],
            "max_happiness":[],
            "max_normality":[],
            "max_appearnce":[],
            "max_interest":[],
            "max_sainity":[],
            "max_importance":[],
            "max_amazing":[],
            "max_c1":[],
            "max_c2":[],
            "max_c3":[],
            "max_c4":[],
            "max_c5":[],
            "max_c6":[],
            "max_c7":[],
            "max_c8":[],
            "max_c9":[],
            "ideal_way_of_speech":[],
            "ideal_socio_economic":[],
            "ideal_ethnicity_skin_color":[],
            "ideal_personality":[],
            "ideal_dress_propeties":[],
            "ideal_political_affiliation":[],
            "ideal_hobbies":[],
            "ideal_body_size":[],
            "ideal_intelligence":[],
            "ideal_goodness":[],
            "ideal_age":[],
            "ideal_happiness":[],
            "ideal_normality":[],
            "ideal_appearnce":[],
            "ideal_interest":[],
            "ideal_sainity":[],
            "ideal_importance":[],
            "ideal_amazing":[],
            "ideal_c1":[],
            "ideal_c2":[],
            "ideal_c3":[],
            "ideal_c4":[],
            "ideal_c5":[],
            "ideal_c6":[],
            "ideal_c7":[],
            "ideal_c8":[],
            "ideal_c9":[],
            "profile_way_of_speech":[],
            "profile_socio_economic":[],
            "profile_ethnicity_skin_color":[],
            "profile_personality":[],
            "profile_dress_propeties":[],
            "profile_political_affiliation":[],
            "profile_hobbies":[],
            "profile_body_size":[],
            "profile_intelligence":[],
            "profile_goodness":[],
            "profile_age":[],
            "profile_happiness":[],
            "profile_normality":[],
            "profile_appearnce":[],
            "profile_interest":[],
            "profile_sainity":[],
            "profile_importance":[],
            "profile_amazing":[],
            "profile_c1":[],
            "profile_c2":[],
            "profile_c3":[],
            "profile_c4":[],
            "profile_c5":[],
            "profile_c6":[],
            "profile_c7":[],
            "profile_c8":[],
            "profile_c9":[],
        }'''

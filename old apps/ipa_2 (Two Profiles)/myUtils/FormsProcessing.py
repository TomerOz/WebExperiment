import ipdb

class FormsProcessor(object):
    def __init__(self, GameMatrix):
        self.GameMatrix = GameMatrix
        self.phase_to_form_processor = {
            "Consent phase" : self._process_consent_form,
            "Matrix tutorial" : self._process_matrix_tutorial_form,
            "Identification Task" : self._process_identification_task,
            "Demographics"         : self._process_demographics,

        }



    def process_form(self, phase_name, post_data):
        if phase_name in self.phase_to_form_processor:
            phase_form_processor = self.phase_to_form_processor[phase_name]
            return phase_form_processor(post_data) # returns a list of form errors if any
        else:
            return [] # returns an empty list -  no form verification is needed

    def _process_demographics(self, post_data):
        errors = []
        if post_data["age"]=='':
            errors.append("חובה לציין גיל")
        if post_data["education"]=="השכלה":
            errors.append("חובה לציין השכלה")
        return errors
    # checks if consent form was filled correctly - returns a list of errors
    def _process_consent_form(self, post_data):
        consent_form_fields = {
                                "Checkbox" : "יש לענות על כלל התנאים על מנת להשתתף בניסוי",
                                }
        errors = []
        for field in consent_form_fields.keys():
            if not field in post_data:
                errors.append(consent_form_fields[field])

        return errors

    def _process_matrix_tutorial_form(self, post_data):
        game = self.GameMatrix.objects.get(phase__name="Matrix tutorial")
        payoffs = game.get_payoffs_dictionary()
        errors = []
        for key in payoffs:
            if payoffs[key] != int(post_data[key]):
                errors.append(key)
        return errors

    def _process_identification_task(self, post_data):
        errors = []
        ALLOWED_MISTAKES_PROPORTION = 0.2
        profilesSides = post_data["profilesSides"][:-1].split(",") # ignoring the last comma
        responses = post_data["responses"][:-1].split(",") # ignoring the last comma
        for i in range(len(profilesSides)):
            left,right = tuple(profilesSides[i].split("//"))
            if "Artificial" in left and "Artificial" in right:
                if responses[i] != "no one":
                    errors.append("error")
            elif "Artificial" in left:
                if responses[i] != "right":
                    errors.append("error")
            elif "Artificial" in right:
                if responses[i] != "left":
                    errors.append("error")

        if len(errors) > ALLOWED_MISTAKES_PROPORTION*len(responses):
            return errors
        else:
            return [] # indicating to views.py that there were no errors


class PhasesDataSaver(object):
    def __init__(self, FeatureLabels, FeatureValue, MinMaxProfileModel):
        self.FeatureLabels = FeatureLabels
        self.FeatureValue = FeatureValue
        self.MinMaxProfileModel = MinMaxProfileModel
        self.phase_to_saver_function = {
            "During Get Profile1" : self._process_create_new_subject_profile,
            "During Get Profile2" : self._process_create_new_subject_profile,
            "During Profile Presentation": self._save_trials_data,
            "Get Min Max Similarity" : self._process_min_max_similarity,
            "Get Max Similarity Profile" : self._get_min_max_similarity_profile,
            "Get Min Similarity Profile" : self._get_min_max_similarity_profile,
            "Get Ideal Profile" : self._get_min_max_similarity_profile,
            "Identification Task" : self._save_identification_task,
            "Demographics" : self._save_demographics,
        }

    def _save_demographics(self, post_data, subject):
        if not post_data["age"].isnumeric():
            age = 0
        else:
            age = int(post_data["age"])
        subject.age = age
        subject.education = post_data["education"]
        subject.save()

    def _save_identification_task(self, post_data, subject):
        subject.subject_profile_sides += post_data["profilesSides"]
        subject.subject_reported_sides += post_data["responses"]
        subject.identification_rts += post_data["reactionTimes"]
        subject.identification_profiles_left += post_data["profilesListLeft"]
        subject.identification_profiles_right += post_data["profilesListRight"]
        subject.save()

    def save_posted_data(self, phase_name, post_data, subject):
        if phase_name in self.phase_to_saver_function:
            save_phase_data = self.phase_to_saver_function[phase_name]
            save_phase_data(post_data, subject) # returns a list of form errors if any

    def _save_trials_data(self, post_data, subject):
        subject.trials_responses_list += post_data["responses"]
        subject.profile_names_left += post_data["profilesListLeft"]
        subject.profile_names_right += post_data["profilesListRight"]
        subject.profiles_response_times += post_data["reactionTimes"]
        subject.trial_features_order += post_data["trialFeatureOrder"]
        subject.subject_profile_sides += post_data["profilesSides"]
        subject.trials_set += post_data["trials_set"]
        subject.save()

    # Fills subject model with posted features provided by the subject user (subject profile witg default values already exists)
    def _process_create_new_subject_profile(self, post_data, new_subject):
        # new_subject.featurevalue_set.all().delete() #
        # shuld be cahnged 12.07.22
        ########################### Mind which features set to choose from! 13.07.21

        if new_subject.current_phase.name == "During Get Profile1":
            label_set = new_subject.sets_order.split(",")[0]
        else:
            label_set = new_subject.sets_order.split(",")[1]

        # deeleting existing features data on this profile if re-entered
        for feature in new_subject.featurevalue_set.all():
            if feature.target_feature.label_set == label_set:
                feature.delete()

        feaure_labels = self.FeatureLabels.objects.filter(label_set=label_set).values_list("feature_name", flat=True)
        ###########################
        for feature_name in feaure_labels:
            feature = self.FeatureLabels.objects.get(feature_name=feature_name)
            feature_value = int(post_data[feature_name])
            subject_feature = self.FeatureValue(target_profile=new_subject, target_feature=feature, value=feature_value)
            subject_feature.save()
            new_subject.save(force_update=True)

    def _get_min_max_similarity_profile(self, post_data, subject):
        if post_data["form_phase"] == "Get Max Similarity Profile":
            profile_name = "Max"
        elif post_data["form_phase"] == "Get Ideal Profile":
            profile_name = "Ideal"
        else:
            profile_name = "Min"
        min_max_profile_full_name = profile_name+"-Subject-"+str(subject.subject_num)
        self.MinMaxProfileModel.objects.filter(target_subject=subject, name=min_max_profile_full_name).delete() # first_deleting an existing profile
        profile = self.MinMaxProfileModel(name=min_max_profile_full_name, profile_label_set=subject.profile_label_set, target_subject=subject)
        profile.is_MinMax = True
        profile.profile_label_set = subject.profile_label_set
        profile.save()
        feaure_labels = self.FeatureLabels.objects.filter(label_set=subject.profile_label_set).values_list("feature_name", flat=True)
        for feature_name in feaure_labels:
            feature = self.FeatureLabels.objects.get(feature_name=feature_name)
            feature_value = int(post_data[feature_name])
            profile_feature = self.FeatureValue(target_profile=profile, target_feature=feature, value=feature_value)
            profile_feature.save()
            profile.save(force_update=True)

    def _process_min_max_similarity(self, post_data, subject):
        subject.max_similarity_name = post_data["maxSimilarityName"]
        subject.max_similarity_value = post_data["similarityInputMax"]
        subject.min_similarity_name = post_data["minSimilarityName"]
        subject.min_similarity_value = post_data["similarityInputMin"]
        subject.save()

import ipdb

class FormsProcessor(object):
    def __init__(self):
        self.phase_to_form_processor = {
            "Consent phase" : self._process_consent_form,
            "Matrix tutorial" : self._process_matrix_tutorial_form,
        }

    def process_form(self, phase_name, post_data):
        if phase_name in self.phase_to_form_processor:
            phase_form_processor = self.phase_to_form_processor[phase_name]
            return phase_form_processor(post_data) # returns a list of form errors if any
        else:
            return [] # returns an empty list -  no form verification is needed

    # checks if consent form was filled correctly - returns a list of errors
    def _process_consent_form(self, post_data):
        consent_form_fields = {
                                "ReadCheckbox" : "You have to read this consent form entirely",
                                "18Checkbox": "You must be 18 to continue",
                                "freeWillCheckbox": "Participation is allowed only under free free will",
                                "privacyPolicy": "You must read the privacy policy and agree to its terms",
                                }
        errors = []
        for field in consent_form_fields.keys():
            if not field in post_data:
                errors.append(consent_form_fields[field])

        return errors

    def _process_matrix_tutorial_form(self, post_data):
        ipdb.set_trace()


class PhasesDataSaver(object):
    def __init__(self, FeatureLabels, FeatureValue):
        self.FeatureLabels = FeatureLabels
        self.FeatureValue = FeatureValue
        self.phase_to_saver_function = {
            "During Get Profile" : self._process_create_new_subject_profile,
            "During Profile Presentation": self._save_trials_data,
        }

    def save_posted_data(self, phase_name, post_data, subject):
        if phase_name in self.phase_to_saver_function:
            save_phase_data = self.phase_to_saver_function[phase_name]
            save_phase_data(post_data, subject) # returns a list of form errors if any

    def _save_trials_data(self, post_data, subject):
        subject.trials_responses_list += post_data["responses"]
        subject.save()

    # Fills subject model with posted features provided by the subject user (subject profile witg default values already exists)
    def _process_create_new_subject_profile(self, post_data, new_subject):
        new_subject.featurevalue_set.all().delete() # deeleting existing features data on this profile if re-entered
        feaure_labels = self.FeatureLabels.objects.values_list("feature_name", flat=True)
        for feature_name in feaure_labels:
            feature = self.FeatureLabels.objects.get(feature_name=feature_name)
            feature_value = int(post_data[feature_name])
            subject_feature = self.FeatureValue(target_profile=new_subject, target_feature=feature, value=feature_value)
            subject_feature.save()
            new_subject.save(force_update=True)

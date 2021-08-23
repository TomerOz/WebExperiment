import os
import ipdb
import pandas as pd

class SubjectData(object):
    def save_subject_data(self, subject, ProfileModel, MinMaxProfileModel, ArtificialProfileModel):
        CURRENT_APP_NAME = 'ipa_1_2'
        path_to_empty_session_df = os.path.join(CURRENT_APP_NAME,"myUtils","empty_session_df.xlsx")
        empty_session_df = pd.read_excel(path_to_empty_session_df)
        ipdb.set_trace()

    def get_profile_features(self):
        "profile_" "min_" "max_" "self_" "ideal_"
        features = pd.read_excel(os.path.join(CURRENT_APP_NAME,"myUtils","features.xlsx")).feature.values

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
        "shapes-1"
        "shapes-2"
        "signs-1"
        "drink-1"
        "drink-2"
        "taste"
        "symbols"
        "number"
        "pattern"

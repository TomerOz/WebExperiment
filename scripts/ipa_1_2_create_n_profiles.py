import ipdb
import pandas as pd
import os
import random

from ipa_1_2.models import *
CURRENT_APP_NAME = "ipa_1_2"

def run():
    def create_n_pilot_profiles(n):
        for i in range(n):
            profile = ProfileModel(name="pilot-"+str(i), profile_label_set="B")
            profile.save()
            feaure_labels = FeatureLabels.objects.filter(label_set="B").values_list("feature_name", flat=True)
            for feature_name in feaure_labels:
                feature = FeatureLabels.objects.get(feature_name=feature_name)
                feature_value = random.randint(0,100)
                profile_feature = FeatureValue(target_profile=profile, target_feature=feature, value=feature_value)
                profile_feature.save()
                profile.save(force_update=True)

    path = os.path.join(CURRENT_APP_NAME,"myUtils","features.xlsx")
    features_df = pd.read_excel(path)
    features_names = features_df.feature.tolist()

    create_n_pilot_profiles(3)

#py manage.py runscript load_inital_data

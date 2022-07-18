import ipdb
import os
import pandas as pd
import numpy as np

class AnalyzeData(object):
    def __init__(self, df_subject_path):
        self.data_path = r"ipa_2/static/ipa_2/data/"
        self.df_subject = pd.read_excel(df_subject_path)

    def find_subject_df(self, subject_number):
        files = os.listdir(self.data_path)
        file_format = 'Subject-' + str(subject_number) + '-'
        for subject_file in files:
            if file_format in subject_file:
                pass

    def get_subject_bonus(self):
        df = self.df_subject
        profiles_phase = df.loc[df["trial_task"]=="profiles",:]
        checked_doubles = []
        double_values = []
        double_rows = pd.DataFrame()
        for i, row in profiles_phase.iterrows():
            p = row.trial_profile
            rows = profiles_phase.loc[profiles_phase['trial_profile'] == p]
            if len(rows) > 1 and p not in checked_doubles:
                checked_doubles.append(p)
                double_rows = double_rows.append(rows)
                double_values.append(rows.response_value.values)

        val_scores = []
        for val in double_values:
            val_score = 100 - abs((int(max(val)) - int(min(val))))
            val_scores.append(val_score)
        return np.mean(val_scores)

import ipdb
import os
import pandas as pd
import numpy as np

data_path = r"ipa_1_2/static/ipa_1_2/data/"
files = os.listdir(data_path)
subject_number = 2
file_format = 'Subject-' + str(subject_number) + '-'
for subject_file in files:
    if file_format in subject_file:
        pass
        #ipdb.set_trace()

trypath = r"ipa_1_2/myUtils/tryData"
file = "Subject-99119-Data.xlsx"

df = pd.read_excel(os.path.join(trypath,file))
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
    val_score = 100 - (int(max(val)) - int(min(val)))
    val_scores.append(val_score)
    ipdb.set_trace()

np.mean(val_scores)

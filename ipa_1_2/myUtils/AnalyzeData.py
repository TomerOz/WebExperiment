import ipdb
import os
import pandas as pd

data_path = "ipa_1_2/static/ipa_1_2/data/"
files = os.listdir(data_path)
subject_number = 2
file_format = 'Subject-' + str(subject_number) + '-'
for subject_file in files:
    if file_format in subject_file:
        ipdb.set_trace()

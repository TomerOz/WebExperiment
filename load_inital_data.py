import ipdb
import pandas as pd

def create_feature_labels():
    features = [
                ["Political Affiliation", "Right wing", "Left wing"],
                ["Hobbies", "Outdoor", "Indoor"],
                ["Body Size", "Small", "Big"],
                ["Intelligece", "Normal", "Very Heigh"],
    ]
    for feature_list in features:
        feature_query = FeatureLabels.objects.filter(feature_name=feature_list[0])
        if len(feature_query) == 0:
            new_feature = FeatureLabels(feature_name=feature_list[0], right_end=feature_list[1], left_end=feature_list[2])
            new_feature.save()

def create_experiment_instance():
    exp_query = Experiment.objects.filter(name="SGS1")
    if len(exp_query) == 0:
        new_exp = Experiment(name="SGS1")
        new_exp.save()

def create_experiment_phases():
    sgs1_phases = ["Consent phase", "Pre Task",
                "Pre Get Profile", "During Get Profile", "Matrix tutorial",
                "Pre Profile Presentation", "During Profile Presentation",
                "end"]
    for i, phase in enumerate(sgs1_phases):
        phase_query = ExperimentPhase.objects.filter(name=phase)
        experiment = Experiment.objects.get(name="SGS1")
        if len(phase_query) == 0:
            new_phase = ExperimentPhase(name=phase, phase_place=i+1, experiment=experiment)
            new_phase.save()

def processs_instructions_df():
    instructions_df = pd.read_excel(r'profilePresntaion\myUtils\instructions.xlsx')
    last_phase = None
    phase_counter = 1
    for index, row in instructions_df.iterrows():
        if last_phase == row.phase:
            phase_counter += 1
        else:
            phase_counter = 1
        last_phase = row.phase
        phase = ExperimentPhase.objects.get(name=row.phase)
        off_order_place = row.off_order_place
        int_place = phase_counter
        if row.off_order_place != "irrelevant":
            int_place = 999
        instruction_query = Instruction.objects.filter(str_phase=phase, int_place=int_place, off_order_place=off_order_place)
        if len(instruction_query) == 0:
            new_instruction = Instruction()
            new_instruction.int_place = int_place
            new_instruction.instruction_text = row.text_he
            new_instruction.str_phase = phase
            new_instruction.experiment = Experiment.objects.get(name="SGS1")
            new_instruction.off_order_place = off_order_place
            new_instruction.is_in_order = True if int_place != 999 else False
            new_instruction.save()

#conda activate exp1 / source exp1/bin/activate
#py manage.py shell;
#from profilePresntaion.models import *
#exec(open('load_inital_data.py').read())
processs_instructions_df()
create_feature_labels()
create_experiment_instance()
create_experiment_phases()

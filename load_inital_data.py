import ipdb
import pandas as pd
import os

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
    sgs1_phases = ["Consent phase", "Pre Task", "Pre Get Profile",
                "During Get Profile", "Identification Task","Matrix tutorial",
                "Pre Profile Presentation", "During Profile Presentation", "end"]

    for i, phase in enumerate(sgs1_phases):
        phase_query = ExperimentPhase.objects.filter(name=phase)
        experiment = Experiment.objects.get(name="SGS1")
        if len(phase_query) == 0:
            new_phase = ExperimentPhase(name=phase, phase_place=i+1, experiment=experiment)
            new_phase.save()

def create_instructinos():
    path = os.path.join("profilePresntaion","myUtils","instructions.xlsx")
    instructions_df = pd.read_excel(path)
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

def create_games_matrices():
    contexts = ["tutorial", "trade", "romantic", "friendship", "conflict"]
    path = os.path.join("profilePresntaion","myUtils","games.xlsx")
    games_df = pd.read_excel(path)
    GameMatrix.objects.all().delete()
    for index, row in games_df.iterrows():
        new_game = GameMatrix()
        new_game.game_name =        row.game_name
        new_game.ps_threshold =     row.ps_threshold
        new_game.strategy_a =       row.strategy_a
        new_game.strategy_b =       row.strategy_b
        new_game.phase =            ExperimentPhase.objects.get(name=row.phase)
        new_game.context_group =    row.context_group
        new_game.pA_Aa =            row.pA_Aa
        new_game.pB_Aa =            row.pB_Aa
        new_game.pA_Ab =            row.pA_Ab
        new_game.pB_Ab =            row.pB_Ab
        new_game.pA_Ba =            row.pA_Ba
        new_game.pB_Ba =            row.pB_Ba
        new_game.pA_Bb =            row.pA_Bb
        new_game.pB_Bb =            row.pB_Bb
        new_game.save()

#conda activate exp1 (at localhost)/ source exp1/bin/activate (at server)
#py manage.py shell;
#from profilePresntaion.models import *
#exec(open('load_inital_data.py').read())
create_instructinos()
create_feature_labels()
create_experiment_instance()
create_experiment_phases()
create_games_matrices()

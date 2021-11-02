import ipdb
import pandas as pd
import os
import random

from ipa_1_2.models import *

CURRENT_APP_NAME = "ipa_1_2"
EXPERIMENT_NAME = "IPA1.2"
IS_UPDATE = True

def run():
    def _get_txt_list(path_and_file, splitter):
        with open(path_and_file,'r') as f:
            list = f.read().split(splitter)
        f.close()
        return list

    def create_feature_labels(features_df):
        global IS_UPDATE
        if not IS_UPDATE:
            FeatureLabels.objects.all().delete()
        for index, row in features_df.iterrows():
            if not IS_UPDATE:
                new_feature = FeatureLabels(feature_name=row.feature)
            else:
                new_feature = FeatureLabels.objects.get(feature_name=row.feature)
            new_feature.right_end=row.right_end
            new_feature.left_end=row.left_end
            new_feature.label_set=row.set
            new_feature.question_heb_male = row.question_heb_male
            new_feature.question_heb_female = row.question_heb_female
            new_feature.question_heb_max_min_ideal_male = row.question_heb_max_min_ideal_male
            new_feature.question_heb_max_min_ideal_female = row.question_heb_max_min_ideal_female
            new_feature.presenting_name = row.presenting_name
            new_feature.save()

    def create_sham_questions(sham_df):
        ShamQuestion.objects.all().delete()
        for index, row in sham_df.iterrows():
            feature_query = ShamQuestion.objects.filter(sham_name=row.feature)
            if len(feature_query) == 0:
                new_feature = ShamQuestion(sham_name=row.feature, right_end=row.right_end, left_end=row.left_end, label_set=row.set)
                new_feature.question_heb_female = row.question_heb_female
                new_feature.question_heb_male = row.question_heb_male
                new_feature.presenting_name = row.presenting_name
                new_feature.save()

    def create_experiment_instance():
        exp_query = Experiment.objects.filter(name=EXPERIMENT_NAME)
        if len(exp_query) == 0:
            new_exp = Experiment(name=EXPERIMENT_NAME)
            new_exp.save()

    def squezze_in_new_phases():
        ''' adds new phases that were added in the phases.text
            do not handle deletion of phases'''

        experiment = Experiment.objects.get(name=EXPERIMENT_NAME)
        exp_phases = _get_txt_list(os.path.join(CURRENT_APP_NAME,"myUtils", 'phases.txt'), "\n")
        current_phases = ExperimentPhase.objects.all()
        added_phases = 0
        for i, phase in enumerate(exp_phases):
            if len(current_phases.filter(name=phase)) == 0:
                # new phase to add
                new_phase = ExperimentPhase(name=phase, phase_place=i+1+added_phases, experiment=experiment)
                new_phase.save()
                added_phases+=1
            else:
                existing_phase = current_phases.get(name=phase)
                existing_phase.phase_place = i+1+added_phases-1
                existing_phase.save()

        phases_to_remove = [phase for phase in current_phases if not phase.name in exp_phases]
        for phase in phases_to_remove:
            phase.delete()

    def _is_sereis_empty(series):
        if len(series) == 0:
            return True
        elif len(series)==1 and series.isna().values[0]==True:
            return True
        return False

    def _get_trials(phases_trials, phase, col_name):
        trials_list = "---"
        series = phases_trials[phases_trials['phase'] == phase][col_name]
        n = 0
        trials_list = ""

        if not _is_sereis_empty(series):
            values_list = series.values[0].split(", ")
            trials_list = ", ".join(values_list)
            n = len(values_list)

        return trials_list, n

    def create_experiment_phases():
        global IS_UPDATE
        if not IS_UPDATE:
            ExperimentPhase.objects.all().delete()
        exp_phases = _get_txt_list(os.path.join(CURRENT_APP_NAME,"myUtils", 'phases.txt'), "\n")
        path = os.path.join(CURRENT_APP_NAME,"myUtils","phases trials.xlsx")
        phases_trials = pd.read_excel(path)
        for i, phase in enumerate(exp_phases):
            experiment = Experiment.objects.get(name=EXPERIMENT_NAME)
            if not IS_UPDATE:
                new_phase = ExperimentPhase(name=phase, phase_place=i+1, experiment=experiment)
            else:
                new_phase = ExperimentPhase.objects.get(name=phase)
            new_phase.phase_place = i+1
            new_phase.experiment = experiment
            practice_trials_content, n_practice_trials = _get_trials(phases_trials, phase, "practice_trials_content")
            trials_content, n_trials = _get_trials(phases_trials, phase, "trials_content")
            new_phase.n_practice_trials = n_practice_trials
            new_phase.practice_trials_content = practice_trials_content
            new_phase.trials_content = trials_content
            new_phase.n_trials = n_trials
            new_phase.save()

    def create_instructinos(): # Depends on an existing "Experiment" instance of SGS1
        Instruction.objects.all().delete()
        path = os.path.join(CURRENT_APP_NAME,"myUtils","instructions.xlsx")
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
                new_instruction.instruction_text_male = row.text_he_male
                new_instruction.instruction_text_female = row.text_he_female
                new_instruction.str_phase = phase
                new_instruction.experiment = Experiment.objects.get(name=EXPERIMENT_NAME)
                new_instruction.off_order_place = off_order_place
                new_instruction.pitctures_names = row.pitctures_names
                new_instruction.is_in_order = True if int_place != 999 else False
                new_instruction.save()

    def create_contexts():
        contexts = _get_txt_list( os.path.join(CURRENT_APP_NAME,"myUtils",'contexts.txt'), "\n")
        for context in contexts:
            context_query = Context.objects.filter(name=context)
            if len(context_query) == 0:
                new_context = Context(name=context)
                new_context.save()

    def create_models():
        models = pd.read_excel(os.path.join(CURRENT_APP_NAME,"myUtils","models.xlsx"))
        global IS_UPDATE
        if not IS_UPDATE:
            SimilarityContextModel.objects.all().delete()
        for label in ["A", "B", "C"]:
            features = [feature.feature_name for feature in FeatureLabels.objects.filter(label_set=label)]
            for i, row in models.iterrows():
                if not IS_UPDATE:
                    context_model = SimilarityContextModel(context=Context.objects.get(name=row.context), label_set=label)
                    context_model.save()
                else:
                    context_model = SimilarityContextModel.objects.get(context=Context.objects.get(name=row.context), label_set=label)
                for feature in features:
                    if feature in models.columns:
                        feature_label = FeatureLabels.objects.get(feature_name=feature)
                        fw, created = FeatureWeight.objects.get_or_create(feature_label=feature_label, model=context_model, value=row[feature], label_set=label)

    def create_games_matrices():
        contexts = _get_txt_list(os.path.join(CURRENT_APP_NAME,"myUtils",'contexts.txt'), "\n")
        path = os.path.join(CURRENT_APP_NAME,"myUtils","games.xlsx")
        games_df = pd.read_excel(path)
        GameMatrix.objects.all().delete()
        for index, row in games_df.iterrows():
            new_game = GameMatrix()
            new_game.game_name =        row.game_name
            new_game.ps_threshold =     row.ps_threshold
            new_game.strategy_a =       row.strategy_a
            new_game.strategy_b =       row.strategy_b
            new_game.phase =            ExperimentPhase.objects.get(name=row.phase)
            new_game.context_group =    Context.objects.get(name=row.context_group)
            new_game.pA_Aa =            row.pA_Aa
            new_game.pB_Aa =            row.pB_Aa
            new_game.pA_Ab =            row.pA_Ab
            new_game.pB_Ab =            row.pB_Ab
            new_game.pA_Ba =            row.pA_Ba
            new_game.pB_Ba =            row.pB_Ba
            new_game.pA_Bb =            row.pA_Bb
            new_game.pB_Bb =            row.pB_Bb
            new_game.save()


    def create_n_pilot_profiles(n):
        for label in ["A","B","C"]:
            feaure_labels = FeatureLabels.objects.filter(label_set=label).values_list("feature_name", flat=True)
            for i in range(n):
                name="pilot-"+str(i) + "-feature set-"+label
                ProfileModel.objects.filter(name=name, profile_label_set=label).all().delete()
                profile = ProfileModel(name=name, profile_label_set=label)
                profile.save()
                for feature_name in feaure_labels:
                    feature = FeatureLabels.objects.get(feature_name=feature_name)
                    feature_value = random.randint(0,100)
                    profile_feature = FeatureValue(target_profile=profile, target_feature=feature, value=feature_value)
                    profile_feature.save()
                    profile.save(force_update=True)



    #conda activate exp1 (at localhost)/ source exp1/bin/activate (at server)
    #py manage.py shell;
    #from profilePresntaion.models import *
    #exec(open('load_inital_data.py').read())


    path = os.path.join(CURRENT_APP_NAME,"myUtils","features.xlsx")
    features_df = pd.read_excel(path)
    sham_path = os.path.join(CURRENT_APP_NAME,"myUtils","sham_questions.xlsx")
    sham_questions_df = pd.read_excel(sham_path)
    features_names = features_df.feature.tolist()

    create_experiment_instance()
    create_experiment_phases() # updte sensitive
    #squezze_in_new_phases()
    create_instructinos() # deletes all previous instances
    create_feature_labels(features_df) # updte sensitive
    create_sham_questions(sham_questions_df)
    create_contexts()
    create_models() # updte sensitive
    create_n_pilot_profiles(3)

#py manage.py runscript load_inital_data

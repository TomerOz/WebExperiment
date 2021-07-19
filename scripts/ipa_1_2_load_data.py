import ipdb
import pandas as pd
import os

from ipa_1_2.models import *
CURRENT_APP_NAME = "ipa_1_2"

def run():
    def _get_txt_list(path_and_file, splitter):
        with open(path_and_file,'r') as f:
            list = f.read().split(splitter)
        f.close()
        return list

    def create_feature_labels(features_df):
        FeatureLabels.objects.all().delete()
        for index, row in features_df.iterrows():
            feature_query = FeatureLabels.objects.filter(feature_name=row.feature)
            if len(feature_query) == 0:
                new_feature = FeatureLabels(feature_name=row.feature, right_end=row.right_end, left_end=row.left_end, label_set=row.set)
                new_feature.save()

    def create_experiment_instance():
        exp_query = Experiment.objects.filter(name="SGS1")
        if len(exp_query) == 0:
            new_exp = Experiment(name="SGS1")
            new_exp.save()

    def create_experiment_phases():
        ExperimentPhase.objects.all().delete()
        sgs1_phases = _get_txt_list(os.path.join(CURRENT_APP_NAME,"myUtils", 'phases.txt'), "\n")
        for i, phase in enumerate(sgs1_phases):
            phase_query = ExperimentPhase.objects.filter(name=phase)
            experiment = Experiment.objects.get(name="SGS1")
            if len(phase_query) == 0:
                new_phase = ExperimentPhase(name=phase, phase_place=i+1, experiment=experiment)
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
                new_instruction.str_phase = phase
                new_instruction.experiment = Experiment.objects.get(name="SGS1")
                new_instruction.off_order_place = off_order_place
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
        features = [feature.feature_name for feature in FeatureLabels.objects.all()]
        SimilarityContextModel.objects.all().delete()
        for i, row in models.iterrows():
            context_model = SimilarityContextModel(context=Context.objects.get(name=row.context))
            context_model.save()
            for feature in features:
                if feature in models.columns:
                    feature_label = FeatureLabels.objects.get(feature_name=feature)
                    fw, created = FeatureWeight.objects.get_or_create(feature_label=feature_label, model=context_model, value=row[feature])

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

    #conda activate exp1 (at localhost)/ source exp1/bin/activate (at server)
    #py manage.py shell;
    #from profilePresntaion.models import *
    #exec(open('load_inital_data.py').read())


    path = os.path.join(CURRENT_APP_NAME,"myUtils","features.xlsx")
    features_df = pd.read_excel(path)
    features_names = features_df.feature.tolist()

    create_experiment_instance()
    create_experiment_phases()
    create_instructinos()
    create_feature_labels(features_df)
    create_contexts()
    create_models()
    # create_games_matrices()

#py manage.py runscript load_inital_data

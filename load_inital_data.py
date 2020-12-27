import ipdb


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
        if phase_query == 0:
            phase_query = ExperimentPhase(name=phase, phase_place=i+1, experiment=experiment)
            phase_query.save()

create_feature_labels()
create_experiment_instance()
create_experiment_phases()
#py manage.py shell
#from profilePresntaion.models import *
#exec(open('load_inital_data.py').read())

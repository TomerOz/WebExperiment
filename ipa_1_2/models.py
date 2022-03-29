from django.db import models
from django.utils import timezone
import datetime
import pytz
import ipdb

# Profile properties classes
class ProfileModel(models.Model):
    name = models.CharField(max_length=200)
    is_subject = models.BooleanField(default=False)
    is_artificial = models.BooleanField(default=False)
    is_MinMax = models.BooleanField(default=False)
    profile_label_set = models.CharField(max_length=2, default="A")
    #pub_date = models.DateTimeField('date published')
    def __str__(self):
        return ("Profile Model" + "-" + self.name)

    def get_features_dict(self):
        features_dictionariy  = {}
        feature_values = self.featurevalue_set.all()
        for fval in feature_values:
            features_dictionariy.setdefault(fval.target_feature.feature_name, fval.value)
        return features_dictionariy

class FeatureLabels(models.Model):
    right_end = models.CharField(max_length=200, default="right")
    left_end = models.CharField(max_length=200, default="left")
    feature_name = models.CharField(max_length=200, default="Name")
    label_set = models.CharField(max_length=2, default="A") # normal features, blog extracted, or meaningless
    question_heb_male = models.CharField(max_length=200, default="Default question?")
    question_heb_female = models.CharField(max_length=200, default="Default question?")
    question_heb_max_min_ideal_male = models.CharField(max_length=200, default="Default question?")
    question_heb_max_min_ideal_female = models.CharField(max_length=200, default="Default question?")
    presenting_name = models.CharField(max_length=200, default="Default Name")

    def __str__(self):
        return ("Feature Label" + "-" + self.feature_name)

class ShamQuestion(models.Model):
    right_end = models.CharField(max_length=200, default="right")
    left_end = models.CharField(max_length=200, default="left")
    sham_name = models.CharField(max_length=200, default="Name")
    label_set = models.CharField(max_length=2, default="A") # normal features, blog extracted, or meaningless
    question_heb_male = models.CharField(max_length=200, default="Default question?")
    question_heb_female = models.CharField(max_length=200, default="Default question?")
    presenting_name = models.CharField(max_length=200, default="Default Name")

    def __str__(self):
        return ("Sham Question" + "-" + self.feature_name)

class FeatureValue(models.Model):
    target_profile = models.ForeignKey(ProfileModel, on_delete=models.CASCADE)
    target_feature = models.ForeignKey(FeatureLabels, on_delete=models.CASCADE)
    value = models.IntegerField()

    def __str__(self):
        return (self.target_profile.name + " " + self.target_feature.feature_name + " " + str(self.value))

#  Experiment backend models
class Experiment(models.Model):
    name = models.CharField(max_length=30, default="")
    phases = models.CharField(max_length=30, default="pre task, post task")
    n_identification_rounds_allowed = models.IntegerField(default=2)
    dubbled_artificials_list = models.CharField(max_length=100, default="0.2, 0.4, 0.6, 0.8")
    subject_bonuses = models.TextField(default="9999-0,")

    def __str__(self):
        return (self.name)

class Context(models.Model):
    name = models.CharField(max_length=30, default="Neutral")

    def __str__(self):
        return (self.name + " Context")

class SimilarityContextModel(models.Model):
    context = models.ForeignKey(Context, on_delete=models.CASCADE)
    label_set = models.CharField(max_length=2, default="A") # normal features, blog extracted, or meaningless

    def __str__(self):
        return ("Similarity Weights Model of " + self.context.name  + " Context")

class FeatureWeight(models.Model):
    feature_label = models.ForeignKey(FeatureLabels, on_delete=models.CASCADE)
    model = models.ForeignKey(SimilarityContextModel, on_delete=models.CASCADE)
    value = models.FloatField(default=0.5)
    label_set = models.CharField(max_length=2, default="A")

    def __str__(self):
        return ("W " + self.feature_label.feature_name+ " - " + self.model.context.name)

class ExperimentPhase(models.Model):
    name = models.CharField(max_length=30, default="")
    phase_place = models.IntegerField()
    experiment = models.ForeignKey(Experiment, on_delete=models.CASCADE) # To wich experiment it is related
    n_trials = models.IntegerField(default=999)
    n_practice_trials = models.IntegerField(default=999)
    practice_trials_content = models.CharField(max_length=1000, default="0.2, 0.5")
    trials_content = models.CharField(max_length=1000, default="0.2, 0.5")

    def _get_list_of_floats_from_string(self, string_list):
        if len(string_list) > 0:
            return [float(i) for i in string_list.split(", ")]
        else:
            return []

    def get_trials_content(self):
        return self._get_list_of_floats_from_string(self.trials_content)

    def get_practice_trials_content(self):
        return self._get_list_of_floats_from_string(self.practice_trials_content)

    def __str__(self):
        return (self.experiment.name + " " + "phase " + self.name + " - " + str(self.phase_place) + " in flow")

class Instruction(models.Model):
    experiment = models.ForeignKey(Experiment, on_delete=models.CASCADE) # To wich experiment it is related
    instruction_text = models.CharField(max_length=1000, default="") # Which text it contains
    int_place = models.IntegerField() # Place in order in case of multiple instructions
    str_phase = models.ForeignKey(ExperimentPhase, on_delete=models.CASCADE) # Description of phase,e.g. "Initial", "Mid break", "Report instrucion"

    is_in_order = models.BooleanField(default=True)
    off_order_place = models.CharField(max_length=40, default="irrelevant")

    instruction_text_male = models.CharField(max_length=1000, default="") # Which text it contains
    instruction_text_female = models.CharField(max_length=1000, default="") # Which text it contains

    pitctures_names = models.CharField(max_length=1000, default="")

    def __str__(self):
        return ("Instruction" + "-" + self.experiment.name + " - " + self.str_phase.name + "-" + str(self.int_place))

# Subject model that stores user responses and behavior as a subject (user - subject connection is encrypted)
class Subject(ProfileModel):
    is_subject = True
    subject_num = models.CharField(max_length=50, default="not_provided")
    experiment = models.ForeignKey(Experiment, on_delete=models.CASCADE)
    completed_experiments = models.CharField(max_length=500, default="-") # a list-like string of experiment -> "SGS1, SGS2,"
    subject_session  = models.IntegerField(default=0) # on creation of subject - session is 1, as in first session.
    context_group = models.CharField(max_length=50, default="neutral") # i.e. romance, conflict, friendship and trade
    current_phase = models.ForeignKey(ExperimentPhase, null=True, on_delete=models.SET_NULL)

    # Min Max profiles similariyt and names:
    max_similarity_value = models.IntegerField(default=999)
    min_similarity_value = models.IntegerField(default=999)
    max_similarity_name = models.CharField(max_length=50, default="not_provided")
    min_similarity_name = models.CharField(max_length=50, default="not_provided")

    # profiles assesment - similarity reports:
    trials_string_list = models.TextField(default="-")
    trials_responses_list = models.TextField(default="-")
    profiles_response_times = models.TextField(default="-")
    feature_response_times = models.TextField(default="-")
    trial_features_order = models.TextField(default="-")

    # identification task:
    subject_profile_sides = models.TextField(default="-")
    subject_reported_sides = models.TextField(default="-")
    identification_rts = models.TextField(default="-")
    identification_profiles = models.TextField(default="-")

    start_time = models.DateTimeField(null=True)
    end_time = models.DateTimeField(null=True)

    # Demograpics
    gender = models.CharField(max_length=20, default="male")
    age = models.IntegerField(default=999)
    education = models.CharField(max_length=20, default="BA")

    n_identification_task_rounds = models.IntegerField(default=0)

    runningLocation = models.CharField(max_length=20, default="Lab") # or home

    #session_1_ps = models.FloatField(default=0.5)
    #session_2_ps = models.FloatField(default=0.5)
    # session_to_ps = #mapping session to randomly assigned ps

    def __str__(self):
        return ("Subject Model" + "-" + self.subject_num)

    def update_subject_session_on_complete(self):
        tz = pytz.timezone("Israel")
        self.end_time = tz.localize(datetime.datetime.now())
        self.completed_experiments = self.completed_experiments + self.experiment.name + ","
        self.save()

class ArtificialProfileModel(ProfileModel):
    '''
        Holds artificial profiles the belong to specic subject.
        Additional propeties:
            name, is_artificial(default=true)
    '''
    is_artificial = True
    target_subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    target_phase =  models.ForeignKey(ExperimentPhase, on_delete=models.CASCADE, default=None)

    def __str__(self):
        return (self.name)

    def get_name_pattern(self, target_similarity, name_instance):
        return "Artificial-" + str(target_similarity) + "-" + name_instance + "-Subject-" + self.target_subject.subject_num

class MinMaxProfileModel(ProfileModel):
    '''
        Holds profiles of max and min similarity reported by a specic subject.
        Additional propeties:
            name, is_subject(default=true)
    '''
    is_MinMax = True
    target_subject = models.ForeignKey(Subject, on_delete=models.CASCADE)

    def __str__(self):
        return (self.name + " - of - " + self.target_subject.name)

class GameMatrix(models.Model):
    game_name = models.CharField(max_length=30, default="no assigned name") # e.g. PD, Chicken
    ps_threshold = models.FloatField()
    is_subject_play_row = models.BooleanField(default=True)
    cooperation_row = models.FloatField(default=0) # 0 top, 1 bottom
    cooperation_col = models.FloatField(default=0) # 0 left, 1 right
    strategy_a = models.CharField(max_length=30, default="cooperate")
    strategy_b = models.CharField(max_length=30, default="defect")
    phase = models.ForeignKey(ExperimentPhase, null=True, on_delete=models.SET_NULL)
    context_group = models.ForeignKey(Context, on_delete=models.CASCADE)

    pA_Aa = models.IntegerField(default=1)
    pB_Aa = models.IntegerField(default=2)
    pA_Ab = models.IntegerField(default=3)
    pB_Ab = models.IntegerField(default=4)
    pA_Ba = models.IntegerField(default=5)
    pB_Ba = models.IntegerField(default=6)
    pA_Bb = models.IntegerField(default=7)
    pB_Bb = models.IntegerField(default=8)


    def get_ps_threshold(self):
        return self.ps_threshold

    def get_payoffs_dictionary(self):
        payoffs_dict = {
            "pA_Aa": self.pA_Aa,
            "pB_Aa": self.pB_Aa,
            "pA_Ab": self.pA_Ab,
            "pB_Ab": self.pB_Ab,
            "pA_Ba": self.pA_Ba,
            "pB_Ba": self.pB_Ba,
            "pA_Bb": self.pA_Bb,
            "pB_Bb": self.pB_Bb,
        }
        return payoffs_dict

    def __str__(self):
        return ("Game Matrix" + "-" + self.game_name + " " + self.context_group.name + ": Ps " + str(self.get_ps_threshold()))


from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

class UserToSubject(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    subject_num = models.CharField(max_length=100, default="not provided")
    features_set = models.CharField(max_length=100, default="A")
    education = models.CharField(max_length=100, default="BA")
    age = models.IntegerField(default=999)
    gender = models.CharField(max_length=100, default="female")
    runningLocation = models.CharField(max_length=20, default="Lab") # or home

    def __str__(self):
        return (self.user.username + "- Subject-" + self.subject_num)

@receiver(post_save, sender=User)
def create_user_subject(sender, instance, created, **kwargs):
    if created:
        if instance.first_name=="IPA_1.2":
            UserToSubject.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_subject(sender, instance, **kwargs):
    try:
        instance.usertosubject.save()
    except:
        pass

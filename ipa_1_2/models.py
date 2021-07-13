from django.db import models

# Profile properties classes
class ProfileModel(models.Model):
    name = models.CharField(max_length=200)
    is_subject = models.BooleanField(default=False)
    is_artificial = models.BooleanField(default=False)
    profile_label_set = models.CharField(max_length=2, default="A")
    #pub_date = models.DateTimeField('date published')
    def __str__(self):
        return ("Profile Model" + "-" + self.name)


class FeatureLabels(models.Model):
    right_end = models.CharField(max_length=200, default="right")
    left_end = models.CharField(max_length=200, default="left")
    feature_name = models.CharField(max_length=200, default="Name")
    label_set = models.CharField(max_length=2, default="A") # normal features, blog extracted, or meaningless

    def __str__(self):
        return ("Feature Label" + "-" + self.feature_name)

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

    def __str__(self):
        return (self.name)

class Context(models.Model):
    name = models.CharField(max_length=30, default="Neutral")

    def __str__(self):
        return (self.name + " Context")

class SimilarityContextModel(models.Model):
    context = models.ForeignKey(Context, on_delete=models.CASCADE)

    def __str__(self):
        return ("Similarity Weights Model of " + self.context.name  + " Context")

class FeatureWeight(models.Model):
    feature_label = models.ForeignKey(FeatureLabels, on_delete=models.CASCADE)
    model = models.ForeignKey(SimilarityContextModel, on_delete=models.CASCADE)
    value = models.FloatField(default=0.5)

    def __str__(self):
        return ("W " + self.feature_label.feature_name+ " - " + self.model.context.name)

class ExperimentPhase(models.Model):
    name = models.CharField(max_length=30, default="")
    phase_place = models.IntegerField()
    experiment = models.ForeignKey(Experiment, on_delete=models.CASCADE) # To wich experiment it is related

    def __str__(self):
        return (self.experiment.name + " " + "phase " + self.name + " - " + str(self.phase_place) + " in flow")

class Instruction(models.Model):
    experiment = models.ForeignKey(Experiment, on_delete=models.CASCADE) # To wich experiment it is related
    instruction_text = models.CharField(max_length=1000, default="") # Which text it contains
    int_place = models.IntegerField() # Place in order in case of multiple instructions
    str_phase = models.ForeignKey(ExperimentPhase, on_delete=models.CASCADE) # Description of phase,e.g. "Initial", "Mid break", "Report instrucion"

    is_in_order = models.BooleanField(default=True)
    off_order_place = models.CharField(max_length=30, default="irrelevant")

    def __str__(self):
        return ("Instruction" + "-" + self.experiment.name + " - " + self.str_phase.name + "-" + str(self.int_place))

# Subject model that stores user responses and behavior as a subject (user - subject connection is encrypted)
class Subject(ProfileModel):
    is_subject = True
    trials_string_list = models.CharField(max_length=800, default="")
    trials_responses_list = models.CharField(max_length=800, default="")
    experiment = models.ForeignKey(Experiment, on_delete=models.CASCADE)
    current_phase = models.ForeignKey(ExperimentPhase, null=True, on_delete=models.SET_NULL)

    subject_session  = models.IntegerField(default=0) # on creation of subject - session is 1, as in first session.
    completed_experiments = models.CharField(max_length=300, default="") # a list-like string of experiment -> "SGS1, SGS2,"
    context_group = models.CharField(max_length=50, default="trade") # i.e. romance, conflict, friendship and trade
    session_1_ps = models.FloatField(default=0.5)
    session_2_ps = models.FloatField(default=0.5)
    # session_to_ps = #mapping session to randomly assigned ps

    def __str__(self):
        return ("Subject Model" + "-" + self.name)

    def update_subject_session_on_complete(self):
    # a function intended to be called on session end prior to logging out the user.
        if self.subject_session == 1:
            self.subject_session = 2
        elif self.subject_session == 2:
            self.completed_experiments = self.completed_experiments + self.experiment.name + ","
        self.current_phase = "end"
        self.save()

class ArtificialProfileModel(ProfileModel):
    '''
        Holds artificial profiles the belong to specic subject.
        Additional propeties:
            name, is_subject(default=true)
    '''
    is_artificial = True
    target_subject = models.ForeignKey(Subject, on_delete=models.CASCADE)

    def __str__(self):
        return ("Artificial Profile Model" + "-" + self.name + " - of - " + self.target_subject.name)


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

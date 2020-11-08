from django.db import models

# Profile properties classes
class ProfileModel(models.Model):
    name = models.CharField(max_length=200)
    is_subject = models.BooleanField(default=False)

    #pub_date = models.DateTimeField('date published')
    def __str__(self):
        return ("Profile Model" + "-" + self.name)

class FeatureLabels(models.Model):
    right_end = models.CharField(max_length=200, default="right")
    left_end = models.CharField(max_length=200, default="left")
    feature_name = models.CharField(max_length=200, default="Name")

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

    def __str__(self):
        return ("Instruction" + "-" + self.experiment.name + " - " + self.str_phase.name + "-" + str(self.int_place))


# Subject model that stores user responses and behavior as a subject (user - subject connection is encrypted)
class Subject(ProfileModel):
    is_subject = True
    trials_string_list = models.CharField(max_length=800, default="")
    trials_responses_list = models.CharField(max_length=800, default="")
    experiment = models.ForeignKey(Experiment, on_delete=models.CASCADE)

    # def initiate_experiment_phase():
    # def get_experiment_phases

    def __str__(self):
        return ("Subject Model" + "-" + self.name)

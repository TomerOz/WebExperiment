from django.db import models

class ProfileModel(models.Model):
    name = models.CharField(max_length=200)

    #pub_date = models.DateTimeField('date published')
    def __str__(self):
        return ("ProfileModel" + "-" + self.name)

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

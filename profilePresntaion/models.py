from django.db import models

class ProfileModel(models.Model):
    name = models.CharField(max_length=200)

    #pub_date = models.DateTimeField('date published')
    def __str__(self):
        return ("ProfileModel" + "-" + self.name)

class Feature(models.Model):
    right_end = models.CharField(max_length=200, default="a")
    left_end = models.CharField(max_length=200, default="b")
    feature_name = models.CharField(max_length=200, default="c")
    value = models.IntegerField(default=0)

    target_profile = models.ForeignKey(ProfileModel, on_delete=models.CASCADE)

    def __str__(self):
        return (self.feature_name)

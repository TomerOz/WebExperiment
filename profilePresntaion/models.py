from django.db import models

from django.utils import timezone
import datetime

# Create your models here.
class Profile(models.Model):
    profile_name = models.CharField(max_length=200)
    #pub_date = models.DateTimeField('date published')

    def __str__(self):
        return self.profile_name

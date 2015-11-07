from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class team(models.Model):
    teamname = models.CharField(max_length=20, blank=False, unique=True)
    #position = models.IntegerField(blank=False)
    points = models.IntegerField(default=0)
    correct_flags = models.IntegerField(default=0)
    wrong_flags = models.IntegerField(default=0)
    #solved = models.ManyToManyField('challenge')
    class Meta:
        verbose_name_plural = "teams"


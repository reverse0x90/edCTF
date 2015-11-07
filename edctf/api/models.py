from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class ctf(models.Model):
    name = models.CharField(max_length=50, blank=False, unique=True)
    live = models.BooleanField(default=False)
    #challengeboard
    #scoreboard
    class Meta:
        verbose_name_plural = "ctfs"

class challengeboard(models.Model):
    ctf = models.OneToOneField('ctf')
    class Meta:
        verbose_name_plural = "challengeboard"

class category(models.Model):
    name =  models.CharField(max_length=50, blank=False)
    challengeboard = models.ForeignKey('challengeboard')
    class Meta:
        verbose_name_plural = "category"

class challenge(models.Model):
    title = models.CharField(max_length=50, blank=False)
    points = models.IntegerField(default=0)
    description = models.CharField(max_length=500, blank=False)
    #solved = models.ManyToManyField('team', default=None)
    num_solved = models.IntegerField(default=0)
    category = models.ForeignKey('category')
    class Meta:
        verbose_name_plural = "challenges"


class scoreboard(models.Model):
    ctf = models.OneToOneField('ctf')
    numtopteams = models.IntegerField(default=10)
    #topteamsdata # send on request
    class Meta:
        verbose_name_plural = "scoreboards"

class team(models.Model):
    scoreboard = models.ForeignKey('scoreboard')
    #scoreboard = models.ManyToManyField('scoreboard') # possible change to this later?

    teamname = models.CharField(max_length=20, blank=False, unique=True)
    #position send on request
    points = models.IntegerField(default=0)
    correct_flags = models.IntegerField(default=0)
    wrong_flags = models.IntegerField(default=0)
    #solved = models.ManyToManyField('challenge', default=None)
    class Meta:
        verbose_name_plural = "teams"

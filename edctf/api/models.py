from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class ctf(models.Model):
    name = models.CharField(max_length=50, blank=False, unique=True)
    live = models.BooleanField(default=False)
    challengeboard = models.ForeignKey('challengeboard')
    scoreboard = models.ForeignKey('scoreboard')
    class Meta:
        verbose_name_plural = "ctfs"
    def __unicode__(self):
       return '{}'.format(self.name)

class challengeboard(models.Model):
    class Meta:
        verbose_name_plural = "challengeboard"
    def __unicode__(self):
       return '{}'.format(self.id)

class category(models.Model):
    name =  models.CharField(max_length=50, blank=False)
    challengeboard = models.ForeignKey('challengeboard')
    class Meta:
        verbose_name_plural = "category"
    def __unicode__(self):
       return '{}'.format(self.name)

class challenge(models.Model):
    title = models.CharField(max_length=50, blank=False)
    points = models.IntegerField(default=0)
    description = models.CharField(max_length=500, blank=False)
    #solved = models.ManyToManyField('team', default=None)
    num_solved = models.IntegerField(default=0)
    category = models.ForeignKey('category')
    flag = models.CharField(max_length=100, blank=False)
    class Meta:
        verbose_name_plural = "challenges"
    def __unicode__(self):
       return '{} {}'.format(self.title, self.points)

class scoreboard(models.Model):
    numtopteams = models.IntegerField(default=10)
    #topteamsdata # send on request
    class Meta:
        verbose_name_plural = "scoreboards"
    def __unicode__(self):
       return '{}'.format(self.id)

class team(models.Model):
    scoreboard = models.ForeignKey('scoreboard')
    #scoreboard = models.ManyToManyField('scoreboard') # possible change to this later?

    teamname = models.CharField(max_length=20, blank=False, unique=True)
    #position send on request
    points = models.IntegerField(default=0)
    correct_flags = models.IntegerField(default=0)
    wrong_flags = models.IntegerField(default=0)
    solved = models.ManyToManyField('challenge', blank=True)
    user = models.OneToOneField(User)
    class Meta:
        verbose_name_plural = "teams"
    def __unicode__(self):
       return '{}: {}'.format(self.id, self.teamname)


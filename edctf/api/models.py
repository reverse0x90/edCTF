from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class ctf(models.Model):
    name = models.CharField(max_length=50, blank=False, unique=True)
    live = models.BooleanField(default=False)
    challengeboard = models.ManyToManyField('challengeboard', related_name="ctfs", related_query_name="ctf")
    scoreboard = models.ManyToManyField('scoreboard', related_name="ctfs", related_query_name="ctf")
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
    challengeboard = models.ForeignKey('challengeboard', related_name="categories", related_query_name="category")
    class Meta:
        verbose_name_plural = "category"
    def __unicode__(self):
       return '{}'.format(self.name)

class challenge(models.Model):
    category = models.ForeignKey('category', related_name="challenges", related_query_name="challenge")
    title = models.CharField(max_length=50, blank=False)
    points = models.IntegerField(default=0)
    description = models.CharField(max_length=500, blank=False)
    #solved = models.ManyToManyField('team', default=None)
    num_solved = models.IntegerField(default=0)
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
    scoreboard = models.ForeignKey('scoreboard', related_name="teams", related_query_name="team")
    #scoreboard = models.ManyToManyField('scoreboard') # possible change to this later?

    teamname = models.CharField(max_length=20, blank=False, unique=True)
    #position send on request
    points = models.IntegerField(default=0)
    correct_flags = models.IntegerField(default=0)
    wrong_flags = models.IntegerField(default=0)
    solved = models.ManyToManyField('challenge', blank=True, related_name="solved", related_query_name="solved")
    user = models.OneToOneField(User)
    class Meta:
        verbose_name_plural = "teams"
    def __unicode__(self):
       return 'team {}: {}'.format(self.id, self.teamname)


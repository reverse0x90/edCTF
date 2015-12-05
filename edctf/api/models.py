from django.db import models
from django.contrib.auth.models import User
from edctf.api.validators import *
from datetime import datetime
import time


class ctf(models.Model):
  """
  Ctf model class.
  """
  name = models.CharField(max_length=250, unique=True, validators=[validate_no_xss, validate_no_html])
  live = models.BooleanField(default=False)
  challengeboard = models.ManyToManyField('challengeboard', related_name="ctfs", related_query_name="ctf")
  scoreboard = models.ManyToManyField('scoreboard', related_name="ctfs", related_query_name="ctf")
  created = models.DateTimeField(auto_now_add=True)

  class Meta:
    verbose_name_plural = "ctfs"

  def __unicode__(self):
    return '{}'.format(self.name)


class challengeboard(models.Model):
  """
  Challengeboard model class.
  """
  created = models.DateTimeField(auto_now_add=True)

  class Meta:
    verbose_name_plural = "challengeboard"

  def __unicode__(self):
    return '{}'.format(self.id)


class category(models.Model):
  """
  Category model class.
  """
  name = models.CharField(max_length=50, validators=[validate_no_xss, validate_no_html])
  challengeboard = models.ForeignKey('challengeboard', related_name="categories", related_query_name="category")
  created = models.DateTimeField(auto_now_add=True)

  class Meta:
    verbose_name_plural = "categories"

  def __unicode__(self):
    return '{}'.format(self.name)


class challenge(models.Model):
  """
  Challenge model class.
  """
  category = models.ForeignKey('category', related_name="challenges", related_query_name="challenge")
  title = models.CharField(max_length=200, validators=[validate_no_xss, validate_no_html])
  points = models.IntegerField(default=0, validators=[validate_positive])
  description = models.CharField(max_length=10000, validators=[validate_no_xss, validate_tags, validate_attributes])
  flag = models.CharField(max_length=100)
  created = models.DateTimeField(auto_now_add=True)

  def _get_number_solved(self):
    """
    Returns number of solved challenges.
    """
    return self.challengeTimestamps.filter(challenge=self).count()
  numsolved = property(_get_number_solved)

  class Meta:
    verbose_name_plural = "challenges"

  def __unicode__(self):
    return '{} {}'.format(self.title, self.points)


class scoreboard(models.Model):
  """
  Scoreboard model class.
  """
  numtopteams = models.IntegerField(default=10)
  created = models.DateTimeField(auto_now_add=True)

  class Meta:
    verbose_name_plural = "scoreboards"

  def __unicode__(self):
    return '{}'.format(self.id)


class team(models.Model):
  """
  Team model class.
  """
  scoreboard = models.ForeignKey('scoreboard', related_name="teams", related_query_name="team")
  teamname = models.CharField(max_length=60, unique=True, validators=[validate_no_xss, validate_no_html])
  points = models.IntegerField(default=0, validators=[validate_positive])
  correctflags = models.IntegerField(default=0, validators=[validate_positive])
  wrongflags = models.IntegerField(default=0, validators=[validate_positive])
  user = models.OneToOneField(User, related_name="teams", related_query_name="team")
  solved = models.ManyToManyField('challenge', blank=True, related_name="solved", through='challengeTimestamp')
  last_timestamp = models.DateTimeField(default=datetime.fromtimestamp(0))
  created = models.DateTimeField(auto_now_add=True)
    
  class Meta:
    verbose_name_plural = "teams"
    
  def __unicode__(self):
    return 'team {}: {}'.format(self.id, self.teamname)

  def solves(self):
    challengeTimestamps = []
    team_challengeTimestamps = self.challengeTimestamps.all()
    for timestamp in team_challengeTimestamps:
      _time = int(time.mktime(timestamp.created.timetuple()))
      _id = timestamp.challenge.id
      challengeTimestamps.append((_id, _time))
    return challengeTimestamps

  def team(self):
    """
    Alias for teamname.
    Created for ctftime api.
    """
    return self.teamname

  def score(self):
    """
    Alias for points.
    Created for ctftime api.
    """
    return self.points


class challengeTimestamp(models.Model):
  """
  ChallengeTimestamp model class.
  """
  team = models.ForeignKey('team', related_name="challengeTimestamps", related_query_name="challengeTimestamp")
  challenge = models.ForeignKey('challenge', related_name="challengeTimestamps", related_query_name="challengeTimestamp")
  created = models.DateTimeField(auto_now_add=True)

  class Meta:
    verbose_name_plural = "challengeTimestamps"

  def __unicode__(self):
    return 'timestamp {}: {}'.format(self.id, self.created)

from django.db import models
from django.contrib.auth.models import User
from edctf.api.validators import *
from datetime import datetime
import time


class Ctf(models.Model):
  """
  Ctf model class.
  """
  name = models.CharField(max_length=250, unique=True, validators=[validate_no_xss, validate_no_html, validate_ctf_iexact])
  live = models.BooleanField(default=False)
  challengeboard = models.OneToOneField('Challengeboard', related_name='ctfs', related_query_name='ctf')
  scoreboard = models.OneToOneField('Scoreboard', related_name='ctfs', related_query_name='ctf')
  created = models.DateTimeField(auto_now_add=True)

  class Meta:
    verbose_name_plural = 'Ctfs'

  def __unicode__(self):
    return '{}'.format(self.name)


class Challengeboard(models.Model):
  """
  Challengeboard model class.
  """
  created = models.DateTimeField(auto_now_add=True)

  class Meta:
    verbose_name_plural = 'Challengeboards'

  def __unicode__(self):
    return '{}'.format(self.id)


class Category(models.Model):
  """
  Category model class.
  """
  name = models.CharField(max_length=50, unique=True, validators=[validate_no_xss, validate_no_html, validate_category_iexact])
  challengeboard = models.ForeignKey('Challengeboard', related_name='categories', related_query_name='category')
  created = models.DateTimeField(auto_now_add=True)

  class Meta:
    verbose_name_plural = 'Categories'

  def __unicode__(self):
    return '{}'.format(self.name)


class Challenge(models.Model):
  """
  Challenge model class.
  """
  category = models.ForeignKey('Category', related_name='challenges', related_query_name='challenge')
  title = models.CharField(max_length=200, validators=[validate_no_xss, validate_no_html])
  points = models.IntegerField(default=0, validators=[validate_positive])
  description = models.CharField(max_length=10000, validators=[validate_no_xss, validate_tags, validate_attributes])
  flag = models.CharField(max_length=100)
  created = models.DateTimeField(auto_now_add=True)

  def delete(self, *args, **kwargs):
    # get teams before deletion
    solved = self.solved.all()
    for team in solved:
      team.points -= self.points

    super(challenge, self).delete(*args, **kwargs)

    # update teams after deletion
    for team in solved:
      team.save()

  def save(self, *args, **kwargs):
    # get solved teams
    solved = None
    if self.id:
      solved = self.solved.all()

    super(challenge, self).save(*args, **kwargs)

    # update solved teams after changes
    if solved:
      for team in solved:
        team.save()

  def _get_number_solved(self):
    """
    Returns number of solved challenges.
    """
    return self.challenge_timestamps.count()
  numsolved = property(_get_number_solved)

  class Meta:
    verbose_name_plural = 'Challenges'

  def __unicode__(self):
    return '{} {}'.format(self.title, self.points)


class Scoreboard(models.Model):
  """
  Scoreboard model class.
  """
  numtopteams = models.IntegerField(default=10)
  created = models.DateTimeField(auto_now_add=True)

  class Meta:
    verbose_name_plural = 'Scoreboards'

  def __unicode__(self):
    return '{}'.format(self.id)


class Team(models.Model):
  """
  Team model class.
  """
  scoreboard = models.ForeignKey('Scoreboard', related_name='teams', related_query_name='team')
  teamname = models.CharField(max_length=60, unique=True, validators=[validate_no_xss, validate_no_html, validate_team_iexact])
  points = models.IntegerField(default=0, validators=[validate_positive])
  correctflags = models.IntegerField(default=0, validators=[validate_positive])
  wrongflags = models.IntegerField(default=0, validators=[validate_positive])
  user = models.OneToOneField(User, related_name='teams', related_query_name='team')
  solved = models.ManyToManyField('Challenge', blank=True, related_name='solved', through='ChallengeTimestamp')
  last_timestamp = models.DateTimeField(default=datetime.fromtimestamp(0))
  created = models.DateTimeField(auto_now_add=True)

  class Meta:
    verbose_name_plural = 'Teams'

  def __unicode__(self):
    return 'team {}: {}'.format(self.id, self.teamname)

  def save(self, *args, **kwargs):
    self.update_points()
    self.update_last_timestamp()
    super(team, self).save(*args, **kwargs)

  def update_points(self):
    """
    Updates the team's points.  Is not saved.
    """
    if self.id:
      points = 0
      solved = self.solved.all()
      for challenge in solved:
        points += challenge.points
      self.points = points

  def update_last_timestamp(self):
    if self.id:
      timestamp = self.challenge_timestamps.order_by('-created').first()
      if timestamp:
        self.last_timestamp = timestamp.created

  def solves(self):
    challenge_timestamps = []
    team_challenge_timestamps = self.challenge_timestamps.all()
    for timestamp in team_challenge_timestamps:
      _time = int(time.mktime(timestamp.created.timetuple()))
      _id = timestamp.challenge.id
      challenge_timestamps.append((_id, _time))
    return challenge_timestamps

  def lasttimestamp(self):
    timestamp = self.challenge_timestamps.order_by('-created').first()
    if not timestamp:
      return 0
    return int(timestamp.created.strftime('%s'))

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


class ChallengeTimestamp(models.Model):
  """
  Challenge Timestamp model class.
  """
  team = models.ForeignKey('team', related_name='challenge_timestamps', related_query_name='challenge_timestamp')
  challenge = models.ForeignKey('challenge', related_name='challenge_timestamps', related_query_name='challenge_timestamp')
  created = models.DateTimeField(auto_now_add=True)

  class Meta:
    verbose_name_plural = 'ChallengeTimestamps'

  def __unicode__(self):
    return 'timestamp {}: {}'.format(self.id, self.created)

from datetime import datetime
from django.contrib.auth.models import User
from django.db import models
from edctf.api.validators import *
import time


class Team(models.Model):
  """
  Team model class.
  """
  scoreboard = models.ForeignKey('Scoreboard', on_delete=models.CASCADE, related_name='teams', related_query_name='team')
  teamname = models.CharField(max_length=30)
  username = models.CharField(max_length=30)
  email = models.EmailField()
  points = models.IntegerField(default=0, validators=[validate_positive])
  correctflags = models.IntegerField(default=0, validators=[validate_positive])
  wrongflags = models.IntegerField(default=0, validators=[validate_positive])
  user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='team')
  solved = models.ManyToManyField('Challenge', blank=True, related_name='solved', through='ChallengeTimestamp')
  last_timestamp = models.DateTimeField(default=datetime.fromtimestamp(0))
  created = models.DateTimeField(auto_now_add=True)

  class Meta:
    verbose_name_plural = 'Teams'

  def __unicode__(self):
    return 'team {}: {}'.format(self.id, self.teamname)

  def delete(self, *args, **kwargs):
    self.user.delete()
    self.challenge_timestamps.all().delete()
    super(Team, self).delete(*args, **kwargs)

  def save(self, *args, **kwargs):
    self.update_points()
    self.update_last_timestamp()
    super(Team, self).save(*args, **kwargs)

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

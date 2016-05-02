from Crypto.Cipher import AES
from datetime import datetime
from django.conf import settings
from django.db import models
from django.utils.translation import ugettext_lazy as _
from edctf.api.validators import *
from hashlib import sha256
import time

AES_KEY = sha256(settings.SECRET_KEY).digest()
BS = 16
pad = lambda s: s + (BS - len(s) % BS) * chr(BS - len(s) % BS) 
unpad = lambda s : s[:-ord(s[len(s)-1:])]


class TeamManager(models.Manager):
  """
  Team manager class
  """
  def _encrypt_teamname(self, teamname, salt=''):
    aes = AES.new(AES_KEY, AES.MODE_ECB)
    message = pad("{salt}{teamname}".format(salt=salt, teamname=teamname))
    return aes.encrypt(message).encode('hex')

  def _decrypt_teamname(self, encrypted_teamname, salt=''):
    aes = AES.new(AES_KEY, AES.MODE_ECB)
    return unpad(aes.decrypt(encrypted_teamname.decode('hex')))[len(salt):]

  def encrypt_teamname(self, teamname, ctf):
    """
    Encrypts teamname with salt ctf.id to allow for duplicate teamnames among different ctfs.
    Key is based on django SECRET_KEY, to prevent users from logging with with their encrypted teamnames.
    """
    return self._encrypt_teamname(teamname, str(ctf.id))

  def decrypt_teamname(self, encrypted_teamname, ctf):
    """
    Decrypts encrypted teamname with salt ctf.id.
    """
    return self._decrypt_teamname(encrypted_teamname, str(ctf.id))

  def create_team(self, teamname, user, ctf=None, **extra_fields):
    if ctf:
      team = self.model(
        enc_teamname=self.encrypt_teamname(teamname, ctf),
        teamname=teamname,
        user=user,
        scoreboard=ctf.scoreboard,
        **extra_fields
      )
    else:
      team = self.model(
        enc_teamname=teamname,
        teamname=teamname,
        user=user,
        **extra_fields
      )
    team.save(using=self._db)
    return team


class Team(models.Model):
  """
  Team model class.
  """
  scoreboard = models.ForeignKey('Scoreboard', null=True, on_delete=models.CASCADE, related_name='teams', related_query_name='team')
  enc_teamname = models.CharField(_('teamname'), max_length=256, unique=True)
  teamname = models.CharField(_('unencrypted teamname'), max_length=30, unique=False)
  points = models.IntegerField(default=0, validators=[validate_positive])
  correctflags = models.IntegerField(default=0, validators=[validate_positive])
  wrongflags = models.IntegerField(default=0, validators=[validate_positive])
  user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='team', related_query_name='team')
  solved = models.ManyToManyField('Challenge', blank=True, related_name='solved', through='ChallengeTimestamp')
  last_timestamp = models.DateTimeField(default=datetime.fromtimestamp(0))
  hidden = models.BooleanField(default=False)
  created = models.DateTimeField(auto_now_add=True)

  objects = TeamManager()

  class Meta:
    verbose_name_plural = 'Teams'

  def __unicode__(self):
    return 'team {}: {}'.format(self.id, self.raw_teamname)

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

  def ctfname(self):
    return self.scoreboard.ctfs.name

  def username(self):
    """
    Alias for user.username
    """
    return self.user.username

  def email(self):
    """
    Alias for user.email
    """
    return self.user.email

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

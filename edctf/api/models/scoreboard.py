from django.db import models


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

  def delete(self, *args, **kwargs):
    teams = self.teams.all()
    for team in teams:
      team.delete()
    super(Scoreboard, self).delete(*args, **kwargs)

from django.db import models


class Ctf(models.Model):
  """
  Ctf model class.
  """
  name = models.CharField(max_length=100, unique=True)
  online = models.BooleanField(default=False)
  challengeboard = models.OneToOneField('Challengeboard', on_delete=models.CASCADE, null=True, related_name='ctfs', related_query_name='ctf')
  scoreboard = models.OneToOneField('Scoreboard', on_delete=models.CASCADE, null=True, related_name='ctfs', related_query_name='ctf')
  created = models.DateTimeField(auto_now_add=True)

  class Meta:
    verbose_name_plural = 'Ctfs'

  def __unicode__(self):
    return '{}'.format(self.name)

  def delete(self, *args, **kwargs):
    self.challengeboard.delete()
    self.scoreboard.delete()
    super(Ctf, self).delete(*args, **kwargs)

  def ctftime(self):
    return '/api/ctftime/{id}'.format(id=self.id)

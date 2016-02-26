from django.db import models


class Challengeboard(models.Model):
  """
  Challengeboard model class.
  """
  created = models.DateTimeField(auto_now_add=True)

  class Meta:
    verbose_name_plural = 'Challengeboards'

  def __unicode__(self):
    return '{}'.format(self.id)

  def delete(self, *args, **kwargs):
    self.categories.all().delete()
    super(Challengeboard, self).delete(*args, **kwargs)

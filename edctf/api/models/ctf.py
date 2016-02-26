from django.db import models
from edctf.database import add_ctf, delete_ctf, get_uid


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


class CtfSchema(models.Model):
  """
  Ctf schema model class.
  """
  schema_name = models.CharField(max_length=100, null=True)
  name = models.CharField(max_length=100, unique=True)
  online = models.BooleanField(default=False)

  class Meta:
    verbose_name_plural = 'CtfSchemas'

  def __unicode__(self):
    return '{}'.format(self.schema_name)
  
  def save(self, *args, **kwargs):
    if not self.pk:
      uid = get_uid()
      schema_name = add_ctf(uid)
      if isinstance(schema_name, str):
        self.schema_name = schema_name
    super(CtfSchema, self).save(*args, **kwargs)

  def delete(self, *args, **kwargs):
    super(CtfSchema, self).delete(*args, **kwargs)
    delete_ctf(self.schema_name)

  def challengeboard(self):
    return '{id}'.format(id=self.id)

  def scoreboard(self):
    return '{id}'.format(id=self.id)

  def ctftime(self):
    return '/api/ctftime/{id}'.format(id=self.id)

from django.db import models


class Category(models.Model):
  """
  Category model class.
  """
  name = models.CharField(max_length=50, unique=True)
  challengeboard = models.ForeignKey('Challengeboard', on_delete=models.CASCADE, related_name='categories', related_query_name='category')
  created = models.DateTimeField(auto_now_add=True)

  class Meta:
    verbose_name_plural = 'Categories'

  def __unicode__(self):
    return '{}'.format(self.name)

  def delete(self, *args, **kwargs):
    self.challenges.all().delete()
    super(Category, self).delete(*args, **kwargs)

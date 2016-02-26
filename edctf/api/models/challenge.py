from django.db import models


class Challenge(models.Model):
  """
  Challenge model class.
  """
  category = models.ForeignKey('Category', on_delete=models.CASCADE, related_name='challenges', related_query_name='challenge')
  title = models.CharField(max_length=200)
  points = models.IntegerField(default=0)
  description = models.CharField(max_length=10000)
  flag = models.CharField(max_length=100)
  created = models.DateTimeField(auto_now_add=True)

  class Meta:
    verbose_name_plural = 'Challenges'

  def __unicode__(self):
    return '{} {}'.format(self.title, self.points)

  def delete(self, *args, **kwargs):
    # get teams before deletion
    solved = self.solved.all()
    for team in solved:
      team.points -= self.points

    super(Challenge, self).delete(*args, **kwargs)

    # update teams after deletion
    for team in solved:
      team.save()

  def save(self, *args, **kwargs):
    # get solved teams
    solved = None
    if self.id:
      solved = self.solved.all()

    super(Challenge, self).save(*args, **kwargs)

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

from django.db import models


class ChallengeTimestamp(models.Model):
  """
  Challenge Timestamp model class.
  """
  team = models.ForeignKey('team', on_delete=models.CASCADE, related_name='challenge_timestamps', related_query_name='challenge_timestamp')
  challenge = models.ForeignKey('challenge', on_delete=models.CASCADE, related_name='challenge_timestamps', related_query_name='challenge_timestamp')
  created = models.DateTimeField(auto_now_add=True)

  class Meta:
    verbose_name_plural = 'ChallengeTimestamps'

  def __unicode__(self):
    return 'timestamp {}: {}'.format(self.id, self.created)

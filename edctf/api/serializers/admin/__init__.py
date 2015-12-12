from rest_framework import serializers
from edctf.api.models import *


class CtfSerializer(serializers.ModelSerializer):
  """
  Sets fields for the rest api to serialize in the ctf model.
  """
  class Meta:
    model = ctf
    fields = ('id', 'name', 'live', 'challengeboard', 'scoreboard')

class ChallengeSerializer(serializers.ModelSerializer):
  """
  Sets fields for the rest api to serialize in the challenge model.
  """
  class Meta:
    model = challenge
    fields = ('id', 'title', 'points', 'description', 'solved', 'numsolved', 'category')

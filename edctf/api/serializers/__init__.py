from rest_framework import serializers
from edctf.api.models import *
import admin

class CtfSerializer(serializers.ModelSerializer):
  """
  Sets fields for the rest api to serialize in the Ctf model.
  """
  class Meta:
    model = Ctf
    fields = ('id', 'name', 'online', 'challengeboard', 'scoreboard')


class ChallengeboardSerializer(serializers.ModelSerializer):
  """
  Sets fields for the rest api to serialize in the Challengeboard model.
  """
  class Meta:
    model = Challengeboard
    fields = ('id', 'categories')


class CategorySerializer(serializers.ModelSerializer):
  """
  Sets fields for the rest api to serialize in the Category model.
  """
  class Meta:
    model = Category
    fields = ('id', 'name', 'challenges')


class ChallengeSerializer(serializers.ModelSerializer):
  """
  Sets fields for the rest api to serialize in the Challenge model.
  """
  class Meta:
    model = Challenge
    fields = ('id', 'title', 'points', 'description', 'solved', 'numsolved', 'category')


class ScoreboardSerializer(serializers.ModelSerializer):
  """
  Sets fields for the rest api to serialize in the Scoreboard model.
  """
  class Meta:
    model = Scoreboard
    fields = ('id', 'numtopteams', 'teams')


class TeamSerializer(serializers.ModelSerializer):
  """
  Sets fields for the rest api to serialize in the Team model.
  """
  class Meta:
    model = Team
    fields = ('id', 'teamname', 'points', 'correctflags', 'wrongflags', 'solves', 'lasttimestamp')


class ChallengeTimestampSerializer(serializers.ModelSerializer):
  """
  Sets fields for the rest api to serialize in the
  ChallengeTimestamp model.
  """
  class Meta:
    model = ChallengeTimestamp
    fields = ('id', 'created')


class CtftimeSerializer(serializers.ModelSerializer):
  """
  Sets fields for the rest api to serialize in the team model.
  """
  class Meta:
    model = Team
    fields = ('team', 'score')

from rest_framework import serializers
from edctf.api.models import *
import admin

class ctf_serializer(serializers.ModelSerializer):
  """
  Sets fields for the rest api to serialize in the ctf model.
  """
  class Meta:
    model = ctf
    fields = ('id', 'name', 'live', 'challengeboard', 'scoreboard')


class challengeboard_serializer(serializers.ModelSerializer):
  """
  Sets fields for the rest api to serialize in the challengeboard model.
  """
  class Meta:
    model = challengeboard
    fields = ('id', 'categories')


class category_serializer(serializers.ModelSerializer):
  """
  Sets fields for the rest api to serialize in the category model.
  """
  class Meta:
    model = category
    fields = ('id', 'name', 'challenges')


class challenge_serializer(serializers.ModelSerializer):
  """
  Sets fields for the rest api to serialize in the challenge model.
  """
  class Meta:
    model = challenge
    fields = ('id', 'title', 'points', 'description', 'solved', 'numsolved', 'category')


class scoreboard_serializer(serializers.ModelSerializer):
  """
  Sets fields for the rest api to serialize in the scoreboard model.
  """
  class Meta:
    model = scoreboard
    fields = ('id', 'numtopteams', 'teams')


class team_serializer(serializers.ModelSerializer):
  """
  Sets fields for the rest api to serialize in the team model.
  """
  class Meta:
    model = team
    fields = ('id', 'teamname', 'points', 'correctflags', 'wrongflags', 'solves', 'lasttimestamp')


class challenge_timestamp_serializer(serializers.ModelSerializer):
  """
  Sets fields for the rest api to serialize in the
  challenge_timestamp model.
  """
  class Meta:
    model = team
    fields = ('id', 'created')


class ctftime_team_serializer(serializers.ModelSerializer):
  """
  Sets fields for the rest api to serialize in the team model.
  """
  class Meta:
    model = team
    fields = ('team', 'score')

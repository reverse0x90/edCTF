from rest_framework import serializers
from django.contrib.auth.models import *
from edctf.api.models import *


class ctfSerializer(serializers.ModelSerializer):
  """
  Sets fields for the rest api to serialize in the ctf model.
  """
  class Meta:
    model = ctf
    fields = ('id', 'name', 'live', 'challengeboard', 'scoreboard')


class challengeboardSerializer(serializers.ModelSerializer):
  """
  Sets fields for the rest api to serialize in the challengeboard model.
  """
  class Meta:
    model = challengeboard
    fields = ('id', 'categories')


class categorySerializer(serializers.ModelSerializer):
  """
  Sets fields for the rest api to serialize in the category model.
  """
  class Meta:
    model = category
    fields = ('id', 'name', 'challenges')


class challengeSerializer(serializers.ModelSerializer):
  """
  Sets fields for the rest api to serialize in the challenge model.
  """
  class Meta:
    model = challenge
    fields = ('id', 'title', 'points', 'description', 'solved', 'numsolved', 'category')


class scoreboardSerializer(serializers.ModelSerializer):
  """
  Sets fields for the rest api to serialize in the scoreboard model.
  """
  class Meta:
    model = scoreboard
    fields = ('id', 'numtopteams', 'teams')


class teamSerializer(serializers.ModelSerializer):
  """
  Sets fields for the rest api to serialize in the team model.
  """
  class Meta:
    model = team
    fields = ('id', 'teamname', 'points', 'correctflags', 'wrongflags', 'solves')


class challengeTimestampSerializer(serializers.ModelSerializer):
  """
  Sets fields for the rest api to serialize in the
  challengeTimestamp model.
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

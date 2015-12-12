from rest_framework.serializers import ModelSerializer
from edctf.api.models import Ctf, Challengeboard, Category, Challenge, Scoreboard, Team


class CtfSerializer(ModelSerializer):
  class Meta:
    model = Ctf
    fields = ('id', 'name', 'live', 'challengeboard', 'scoreboard')


class ChallengeboardSerializer(ModelSerializer):
  class Meta:
    model = Challengeboard
    fields = ('id', 'categories')


class CategorySerializer(ModelSerializer):
  class Meta:
    model = Category
    fields = ('id', 'name', 'challenges')


class ChallengeSerializer(ModelSerializer):
  class Meta:
    model = Challenge
    fields = ('id', 'title', 'points', 'description', 'solved', 'numsolved', 'category')


class ScoreboardSerializer(ModelSerializer):
  class Meta:
    model = Scoreboard
    fields = ('id', 'numtopteams', 'teams')


class TeamSerializer(ModelSerializer):
  class Meta:
    model = Team
    fields = ('id', 'teamname', 'points', 'correctflags', 'wrongflags', 'solves', 'lasttimestamp')

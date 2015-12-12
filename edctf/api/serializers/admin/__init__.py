from rest_framework.serializers import ModelSerializer
from edctf.api.models import ctf, challengeboard, category, challenge, scoreboard, team


class CtfSerializer(ModelSerializer):
  class Meta:
    model = ctf
    fields = ('id', 'name', 'live', 'challengeboard', 'scoreboard')

class ChallengeboardSerializer(ModelSerializer):
  class Meta:
    model = challengeboard
    fields = ('id', 'categories')

class CategorySerializer(ModelSerializer):
  class Meta:
    model = category
    fields = ('id', 'name', 'challenges')

class ChallengeSerializer(ModelSerializer):
  class Meta:
    model = challenge
    fields = ('id', 'title', 'points', 'description', 'solved', 'numsolved', 'category')

class ScoreboardSerializer(ModelSerializer):
  class Meta:
    model = scoreboard
    fields = ('id', 'numtopteams', 'teams')

class TeamSerializer(ModelSerializer):
  class Meta:
    model = team
    fields = ('id', 'teamname', 'points', 'correctflags', 'wrongflags', 'solves', 'lasttimestamp')

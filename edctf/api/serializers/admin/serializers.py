from edctf.api.models import Category
from edctf.api.models import Challenge
from edctf.api.models import Challengeboard
from edctf.api.models import Ctf
from edctf.api.models import Scoreboard
from edctf.api.models import Team
from rest_framework.serializers import ModelSerializer


class CategorySerializer(ModelSerializer):
  class Meta:
    model = Category
    fields = ('id', 'name', 'challenges')


class ChallengeSerializer(ModelSerializer):
  class Meta:
    model = Challenge
    fields = ('id', 'title', 'points', 'description', 'solved', 'numsolved', 'category', 'flag')


class ChallengeboardSerializer(ModelSerializer):
  class Meta:
    model = Challengeboard
    fields = ('id', 'categories')


class CtfSerializer(ModelSerializer):
  class Meta:
    model = Ctf
    fields = ('id', 'name', 'online', 'ctftime', 'challengeboard', 'scoreboard')


class ScoreboardSerializer(ModelSerializer):
  class Meta:
    model = Scoreboard
    fields = ('id', 'numtopteams', 'teams')


class TeamSerializer(ModelSerializer):
  class Meta:
    model = Team
    fields = ('id', 'teamname', 'points', 'correctflags', 'wrongflags', 'solves', 'lasttimestamp', 'username', 'email', 'hidden')

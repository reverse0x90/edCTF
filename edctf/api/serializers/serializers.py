from edctf.api.models import Category
from edctf.api.models import Challenge
from edctf.api.models import Challengeboard
from edctf.api.models import ChallengeTimestamp
from edctf.api.models import Ctf
from edctf.api.models import Scoreboard
from edctf.api.models import Team
from rest_framework.serializers import ModelSerializer


class CtfSerializer(ModelSerializer):
  """
  Sets fields for the rest api to serialize in the Ctf model.
  """
  class Meta:
    model = Ctf
    fields = ('id', 'name', 'online', 'challengeboard', 'scoreboard')


class ChallengeboardSerializer(ModelSerializer):
  """
  Sets fields for the rest api to serialize in the Challengeboard model.
  """
  class Meta:
    model = Challengeboard
    fields = ('id', 'categories')


class CategorySerializer(ModelSerializer):
  """
  Sets fields for the rest api to serialize in the Category model.
  """
  class Meta:
    model = Category
    fields = ('id', 'name', 'challenges')


class ChallengeSerializer(ModelSerializer):
  """
  Sets fields for the rest api to serialize in the Challenge model.
  """
  class Meta:
    model = Challenge
    fields = ('id', 'title', 'points', 'description', 'solved', 'numsolved', 'category')


class ScoreboardSerializer(ModelSerializer):
  """
  Sets fields for the rest api to serialize in the Scoreboard model.
  """
  class Meta:
    model = Scoreboard
    fields = ('id', 'numtopteams', 'teams')


class TeamSerializer(ModelSerializer):
  """
  Sets fields for the rest api to serialize in the Team model.
  """
  class Meta:
    model = Team
    fields = ('id', 'teamname', 'points', 'correctflags', 'wrongflags', 'solves', 'lasttimestamp', 'hidden')


class ChallengeTimestampSerializer(ModelSerializer):
  """
  Sets fields for the rest api to serialize in the
  ChallengeTimestamp model.
  """
  class Meta:
    model = ChallengeTimestamp
    fields = ('id', 'created')


class CtftimeSerializer(ModelSerializer):
  """
  Sets fields for the rest api to serialize in the team model.
  """
  class Meta:
    model = Team
    fields = ('team', 'score')

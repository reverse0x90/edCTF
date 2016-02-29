from rest_framework.views import APIView
from rest_framework.response import Response
from edctf.api.models import Scoreboard, Team
from edctf.api.permissions import ScoreboardPermission, ScoreboardPermissionDetail
from edctf.api.serializers import ScoreboardSerializer, TeamSerializer
from edctf.api.serializers.admin import ScoreboardSerializer as AdminScoreboardSerializer
from edctf.api.serializers.admin import TeamSerializer as AdminTeamSerializer
import time


class ScoreboardView(APIView):
  """
  Manages scoreboard requests.
  """
  permission_classes = (ScoreboardPermission,)

  def get(self, request, format=None):
    """
    Get all scoreboards
    """
    scoreboards = Scoreboard.objects.all()
    if request.user.is_staff:
      serialized_scoreboards = AdminScoreboardSerializer(scoreboards, many=True, context={'request': request})
    else:
      serialized_scoreboards = ScoreboardSerializer(scoreboards, many=True, context={'request': request})
    return Response({
      'scoreboards': serialized_scoreboards.data,
    })



class ScoreboardViewDetail(APIView):
  """
  Manages scoreboard requests.
  """
  permission_classes = (ScoreboardPermissionDetail,)

  def get(self, request, id, format=None):
    """
    Get scoreboard by id
    """
    try:
      scoreboard = Scoreboard.objects.get(id=id)
    except ObjectDoesNotExist:
      return error_response('Challengeboard not found')
    teams = scoreboard.teams

    serialized_scoreboard = ScoreboardSerializer(scoreboard, many=True, context={'request': request})
    serialized_teams = TeamSerializer(teams, many=True, context={'request': request})
    return Response({
      'scoreboards': serialized_scoreboard.data,
      'teams': teams_serializer.data,
    })

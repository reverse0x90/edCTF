from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from edctf.api.models import Scoreboard, Team
from edctf.api.serializers import ScoreboardSerializer, TeamSerializer
import time


class ScoreboardView(APIView):
  """
  Manages scoreboard requests.
  """
  permission_classes = (AllowAny,)

  def get(self, request, id=None, format=None):
    """
    Get all scoreboards or gets an individual scoreboard via
    scoreboards/:id
    """
    # If scoreboard id was requested, return that scoreboard else
    # return list of scoreboards.
    if id:
      # Retrieve and serialize the requested scoreboard data.
      scoreboards = Scoreboard.objects.filter(id=id)
      scoreboards_serializer = ScoreboardSerializer(scoreboards, many=True, context={'request': request})

      # Retrieve and serialize the teams on the scoreboard.
      teams = Team.objects.filter(scoreboard=scoreboards.first())
      teams_serializer = TeamSerializer(teams, many=True, context={'request': request})

      # Return the serialized data.
      return Response({
        'scoreboards': scoreboards_serializer.data,
        'teams': teams_serializer.data,
      })
    else:
      # Retrieve and serialize the requested scoreboard data.
      scoreboards = Scoreboard.objects.all()
      scoreboards_serializer = ScoreboardSerializer(scoreboards, many=True, context={'request': request})

      # Return the serialized data.
      return Response({
        'scoreboards': scoreboards_serializer.data,
      })

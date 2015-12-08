from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from edctf.api.models import scoreboard, team
from edctf.api.serializers import scoreboard_serializer, team_serializer
import time


class scoreboard_view(APIView):
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
      scoreboards = scoreboard.objects.filter(id=id)
      scoreboards_serializer = scoreboard_serializer(scoreboards, many=True, context={'request': request})

      # Retrieve and serialize the teams on the scoreboard.
      teams = team.objects.filter(scoreboard=scoreboards[0]).order_by('-points', '-last_timestamp', 'id')
      teams_serializer = team_serializer(teams, many=True, context={'request': request})
      for pos, _team in enumerate(teams_serializer.data):
        _team['position'] = pos+1

      # Return the serialized data.
      return Response({
        "scoreboards": scoreboards_serializer.data,
        "teams": teams_serializer.data,
      })
    else:
      # Retrieve and serialize the requested scoreboard data.
      scoreboards = scoreboard.objects.all()
      scoreboards_serializer = scoreboard_serializer(scoreboards, many=True, context={'request': request})

      # Return the serialized data.
      return Response({
        "scoreboards": scoreboards_serializer.data,
      })

from django.core.exceptions import ObjectDoesNotExist
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework import status
from edctf.api.models import Ctf
from edctf.api.serializers import CtftimeSerializer


class CtftimeView(APIView):
  """
  Returns with ctftime scoreboard.
    https://ctftime.org/json-scoreboard-feed
  """
  permission_classes = (AllowAny,)
  
  def get(self, request, id=None, format=None):
    """
    Gets  minimal ctftime scoreboard according to:
      https://ctftime.org/json-scoreboard-feed
    Requires id of ctf.
    """
    if id:
      try:
        _ctf = Ctf.objects.get(id=id)
      except ObjectDoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

      scoreboard = _ctf.scoreboard.first()
      teams = scoreboard.teams.order_by('-points','last_timestamp', 'id')
      teams_serialized = CtftimeSerializer(teams, many=True, context={'request': request})

      for pos, _team in enumerate(teams_serialized.data):
        _team['pos'] = pos+1

      return Response({
        'standings': teams_serialized.data,
      })
    else:
      return Response(status=status.HTTP_404_NOT_FOUND)

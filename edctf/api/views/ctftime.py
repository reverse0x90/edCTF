from django.core.exceptions import ObjectDoesNotExist
from response import error_response
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from edctf.api.models import Ctf
from edctf.api.permissions import CtftimePermission
from edctf.api.serializers import CtftimeSerializer


class CtftimeViewDetail(APIView):
  """
  Returns with ctftime scoreboard.
    https://ctftime.org/json-scoreboard-feed
  """
  permission_classes = (CtftimePermission,)
  
  def get(self, request, ctf_id, format=None):
    """
    Gets minimal ctftime scoreboard according to:
      https://ctftime.org/json-scoreboard-feed
    Requires ctf id.
    """
    try:
      ctf = Ctf.objects.get(id=ctf_id)
    except ObjectDoesNotExist:
      return error_response('CTF not found')

    teams = ctf.scoreboard.teams.order_by('-points','-last_timestamp', 'created')
    teams_serialized = CtftimeSerializer(teams, many=True, context={'request': request})

    for pos, _team in enumerate(teams_serialized.data):
      _team['pos'] = pos+1

    return Response({
      'standings': teams_serialized.data,
    })

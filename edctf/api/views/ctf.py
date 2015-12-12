from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from edctf.api.models import Ctf
from edctf.api.serializers import CtfSerializer


class CtfView(APIView):
  """
  Manages ctf requests.
  """
  permission_classes = (AllowAny,)
  
  def get(self, request, id=None, format=None):
    """
    Gets all ctfs or gets an individual ctf via ctfs/:id or gets
    all live ctfs via GET parameter, i.e. live=true.
    """
    # If ctf id was requested, return that ctf else return list of
    # all/live ctfs.
    if id:
      ctfs = Ctf.objects.filter(id=id)
    else:
      if 'live' in request.query_params:
        if request.query_params['live'] == 'true':
          ctfs = Ctf.objects.filter(live=True)
        else:
          ctfs = Ctf.objects.filter(live=False)
      else:
        ctfs = Ctf.objects.all()
    serializer = CtfSerializer(ctfs, many=True, context={'request': request})
    return Response({
      'ctfs': serializer.data,
    })

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from edctf.api.models import ctf
from edctf.api.serializers import ctf_serializer


class ctf_view(APIView):
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
      ctfs = ctf.objects.filter(id=id)
    else:
      if 'live' in request.query_params:
        if request.query_params['live'] == 'true':
          ctfs = ctf.objects.filter(live=True)
        else:
          ctfs = ctf.objects.filter(live=False)
      else:
        ctfs = ctf.objects.all()
    serializer = ctf_serializer(ctfs, many=True, context={'request': request})
    return Response({
      'ctfs': serializer.data,
    })

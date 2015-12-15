from django.db import IntegrityError
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response
from edctf.api.models import Ctf, Challengeboard, Scoreboard
from edctf.api.serializers import CtfSerializer
from edctf.api.permissions import CtfPermission, CtfPermissionDetail


class CtfView(APIView):
  """
  Manages ctf requests.
  """
  permission_classes = (CtfPermission,)

  def error_response(self, error, errorfields={}):
    """
    Handles error messages for post
    """
    return Response({
      'errors': {
        'message': error,
        'fields': errorfields,
      },
    }, status=status.HTTP_400_BAD_REQUEST)

  def get(self, request, format=None):
    """
    Gets all ctfs gets the live ctf via GET parameter, i.e. live=true
    """
    if 'live' in request.query_params:
      if request.query_params['live'] == 'true':
        ctfs = Ctf.objects.filter(live=True)
      else:
        ctfs = Ctf.objects.filter(live=False)
    else:
      ctfs = Ctf.objects.all()
    serialized_ctfs = CtfSerializer(ctfs, many=True, context={'request': request})
    return Response({
      'ctfs': serialized_ctfs.data,
    })

  def post(self, request, id=None, format=None):
    """
    Create a new ctf
    """
    # {"ctf":{"name":"e","live":true,"challengeboard":null,"scoreboard":null}}
    if 'ctf' not in request.data or not request.data['ctf']:
      return Response(status=status.HTTP_400_BAD_REQUEST)
    ctf_data = request.data['ctf']

    if 'name' not in ctf_data or not ctf_data['name']:
      return self.error_response('CTF name not given', errorfields={'name': True})
    if 'live' not in ctf_data:
      return self.error_response('CTF live status not given', errorfields={'live': True})

    name = ctf_data['name']
    if ctf_data['live']:
      live = True
    else:
      live = False

    try:
      ctf = Ctf.objects.create(name=name, live=live)#, challengeboard=challengeboard, scoreboard=scoreboard)
    except IntegrityError as e:
      return self.error_response('CTF name already taken', errorfields={'name': True})
    challengeboard = Challengeboard.objects.create()
    scoreboard = Scoreboard.objects.create()

    ctf.challengeboard = challengeboard
    ctf.scoreboard = scoreboard
    ctf.save()

    serialized_ctf = CtfSerializer(ctf, many=False, context={'request': request})

    # disable all other live ctfs
    if live:
      live_ctfs = Ctf.objects.exclude(id=ctf.id).filter(live=True)
      for ctf in live_ctfs:
        ctf.live = False
        ctf.save()

    return Response({
      'ctf': serialized_ctf.data,
    })


class CtfViewDetail(APIView):
  """
  Manages ctf by id requests.
  """
  permission_classes = (CtfPermissionDetail,)
  
  def get(self, request, id, format=None):
    """
    Gets individual ctf via ctfs/:id
    """
    ctf = Ctf.objects.filter(id=id).first()
    serializer = CtfSerializer(ctf, many=False, context={'request': request})
    return Response({
      'ctf': serializer.data,
    })

  def put(self, request, id=None, format=None):
    """
    Edits a ctf
    """
    return Response({
      'ctf': 'test',
    })

  def delete(self, request, id=None, format=None):
    """
    Deletes a ctf
    """
    return Response({
      'ctf': 'test',
    })

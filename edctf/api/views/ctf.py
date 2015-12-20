from django.core.exceptions import ObjectDoesNotExist
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
    Handles error messages
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

    if len(ctf_data['name']) > 100:
      return self.error_response('CTF name too long, over 100 characters', errorfields={'live': True})
    name = str(ctf_data['name'])
    live = True if ctf_data['live'] else False

    if Ctf.objects.filter(name__iexact=name).exists():
      return self.error_response('CTF name already taken', errorfields={'name': True})

    try:
      ctf = Ctf.objects.create(name=name, live=live)
    except IntegrityError:
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

  def error_response(self, error, errorfields={}):
    """
    Handles error messages
    """
    return Response({
      'errors': {
        'message': error,
        'fields': errorfields,
      },
    }, status=status.HTTP_400_BAD_REQUEST)
  
  def get(self, request, id, format=None):
    """
    Gets individual ctf via ctfs/:id
    """
    try:
      ctf = Ctf.objects.get(id=id)
    except ObjectDoesNotExist:
      return self.error_response('CTF not found', errorfields={})

    serialized_ctf = CtfSerializer(ctf, many=False, context={'request': request})
    return Response({
      'ctf': serialized_ctf.data,
    })

  def put(self, request, id, format=None):
    """
    Edits a ctf
    """
    try:
      ctf = Ctf.objects.get(id=id)
    except ObjectDoesNotExist:
      return self.error_response('CTF not found', errorfields={})

    ctf_data = request.data['ctf']
    if 'name' not in ctf_data or not ctf_data['name']:
      return self.error_response('CTF name not given', errorfields={'name': True})
    if 'live' not in ctf_data:
      return self.error_response('CTF live status not given', errorfields={'live': True})

    if len(ctf_data['name']) > 100:
      return self.error_response('CTF name too long, over 100 characters', errorfields={'live': True})

    name = str(ctf_data['name'])
    if ctf.name.lower() != name.lower() and Ctf.objects.filter(name__iexact=name).exists():
      return self.error_response('CTF name already taken', errorfields={'name': True})

    ctf.name = name
    ctf.live = True if ctf_data['live'] else False

    try:
      ctf.save()
    except IntegrityError:
      return self.error_response('CTF name already taken', errorfields={'name': True})

    serialized_ctf = CtfSerializer(ctf, many=False, context={'request': request})
    return Response({
      'ctf': serialized_ctf.data,
    })

  def delete(self, request, id, format=None):
    """
    Deletes a ctf
    """
    try:
      ctf = Ctf.objects.get(id=id)
    except ObjectDoesNotExist:
      return self.error_response('CTF not found', errorfields={})

    if ctf.live:
      return self.error_response('Cannot delete a live ctf', errorfields={})

    ctf.delete()

    # return 200 and empty object on success
    return Response({})

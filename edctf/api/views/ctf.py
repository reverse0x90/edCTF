from django.core.exceptions import ObjectDoesNotExist
from django.db import IntegrityError
from edctf.api.models import Ctf, CtfSchema, Challengeboard, Scoreboard
from edctf.api.serializers import CtfSerializer, CtfSchemaSerializer
from edctf.api.serializers.admin import CtfSerializer as AdminCtfSerializer
from edctf.api.serializers.admin import CtfSchemaSerializer as AdminCtfSchemaSerializer
from edctf.api.permissions import CtfPermission, CtfPermissionDetail
from response import error_response
from rest_framework.views import APIView
from rest_framework.response import Response


class CtfView(APIView):
  """
  Manages ctf requests.
  """
  permission_classes = (CtfPermission,)

  def get(self, request, format=None):
    """
    Gets all ctfs gets the online ctf via GET parameter, i.e. online=true
    """
    if 'online' in request.query_params:
      if request.query_params['online'] == 'true':
        schemas = CtfSchema.objects.using('default').filter(online=True)
      else:
        schemas = CtfSchema.objects.using('default').filter(online=False)
    else:
      schemas = CtfSchema.objects.using('default').all()

    if request.user.is_staff:
      serialized_schemas = AdminCtfSchemaSerializer(schemas, many=True, context={'request': request})
    else:
      serialized_schemas = CtfSchemaSerializer(schemas, many=True, context={'request': request})
    
    return Response({
      'ctfs': serialized_schemas.data,
    })

  def post(self, request, id=None, format=None):
    """
    Create a new ctf
    """
    if 'ctf' not in request.data or not request.data['ctf']:
      return error_response('CTF not given')

    ctf_data = request.data['ctf']
    if 'name' not in ctf_data or not ctf_data['name']:
      return error_response('CTF name not given', errorfields={'name': True})
    if 'online' not in ctf_data:
      return error_response('CTF online status not given', errorfields={'online': True})

    if len(ctf_data['name']) > 100:
      return error_response('CTF name too long, over 100 characters', errorfields={'name': True})
    name = str(ctf_data['name'])
    online = True if ctf_data['online'] else False

    if Ctf.objects.filter(name__iexact=name).exists():
      return error_response('CTF name already taken', errorfields={'name': True})

    try:
      schema = CtfSchema.objects.using('default').create(name=name, online=online)
      if not schema.schema_name:
        return error_response('Error adding CTF', errorfields={'name': True})
      
      ctf = Ctf.objects.using(schema.schema_name).create(name=schema.name, online=schema.online)
    except IntegrityError:
      raise
      return error_response('CTF name already taken', errorfields={'name': True})

    challengeboard = Challengeboard.objects.using(schema.schema_name).create()
    scoreboard = Scoreboard.objects.using(schema.schema_name).create()

    ctf.challengeboard = challengeboard
    ctf.scoreboard = scoreboard
    ctf.save()

    # disable all other online ctfs
    if online:
      online_ctfs = CtfSchema.objects.using('default').exclude(id=schema.id).filter(online=True)
      for ctf_schema in online_ctfs:
        ctf_schema.online = False
        ctf_schema.save()

    if request.user.is_staff:
      serialized_schema = AdminCtfSchemaSerializer(schema, many=False, context={'request': request})
    else:
      serialized_schema = CtfSchemaSerializer(schema, many=False, context={'request': request})
    return Response({
      'ctf': serialized_schema.data,
    })


class CtfViewDetail(APIView):
  """
  Manages ctf by id requests.
  """
  permission_classes = (CtfPermissionDetail,)

  def get(self, request, id, format=None):
    """
    Gets individual ctf via id
    """
    try:
      schema = CtfSchema.objects.using('default').get(id=id)
    except ObjectDoesNotExist:
      return error_response('CTF not found')

    if request.user.is_staff:
      serialized_schema = AdminCtfSchemaSerializer(schema, many=False, context={'request': request})
    else:
      serialized_schema = CtfSchemaSerializer(schema, many=False, context={'request': request})
    return Response({
      'ctf': serialized_schema.data,
    })

  def put(self, request, id, format=None):
    """
    Edits a ctf
    """
    try:
      schema = CtfSchema.objects.using('default').get(id=id)
      if not schema.schema_name:
        return error_response('CTF not found')

      ctf = Ctf.objects.using(schema.schema_name).get(name=schema.name)
    except ObjectDoesNotExist:
      return error_response('CTF not found')

    if 'ctf' not in request.data or not request.data['ctf']:
      return error_response('CTF not given')

    ctf_data = request.data['ctf']
    if 'name' not in ctf_data or not ctf_data['name']:
      return error_response('CTF name not given', errorfields={'name': True})
    if 'online' not in ctf_data:
      return error_response('CTF online status not given', errorfields={'online': True})

    if len(ctf_data['name']) > 100:
      return error_response('CTF name too long, over 100 characters', errorfields={'name': True})

    name = str(ctf_data['name'])
    if ctf.name.lower() != name.lower() and CtfSchema.objects.using('default').filter(name__iexact=name).exists():
      return error_response('CTF name already taken', errorfields={'name': True})
    online = True if ctf_data['online'] else False

    # disable all other online ctfs
    if online:
      online_ctfs = CtfSchema.objects.using('default').exclude(id=schema.id).filter(online=True)
      for ctf_schema in online_ctfs:
        ctf_schema.online = False
        ctf_schema.save()

    ctf.name = name
    ctf.online = online
    schema.name = name
    schema.online = online

    try:
      schema.save()
    except IntegrityError:
      return error_response('CTF name already taken', errorfields={'name': True})

    try:
      ctf.save()
    except IntegrityError:
      return error_response('Error saving CTF', errorfields={'name': True})

    if request.user.is_staff:
      serialized_schema = AdminCtfSchemaSerializer(schema, many=False, context={'request': request})
    else:
      serialized_schema = CtfSchemaSerializer(schema, many=False, context={'request': request})
    return Response({
      'ctf': serialized_schema.data,
    })

  def delete(self, request, id, format=None):
    """
    Deletes a ctf
    """
    try:
      schema = CtfSchema.objects.using('default').get(id=id)
      if not schema.schema_name:
        return error_response('CTF not found')

      ctf = Ctf.objects.using(schema.schema_name).get(name=schema.name)
    except ObjectDoesNotExist:
      return error_response('CTF not found')

    if schema.online:
      return error_response('Cannot delete an online ctf')

    ctf.delete()
    schema.delete()  # need to fix this..doesnt remove schema, since django is using it?

    # return 200 and empty object on success
    return Response({})

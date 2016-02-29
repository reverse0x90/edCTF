from django.core.exceptions import ObjectDoesNotExist
from edctf.api.models import Category, Challenge
from edctf.api.permissions import ChallengePermission, ChallengePermissionDetail
from edctf.api.serializers import ChallengeSerializer
from edctf.api.serializers.admin import ChallengeSerializer as AdminChallengeSerializer
from response import error_response
from rest_framework.views import APIView
from rest_framework.response import Response


class ChallengeView(APIView):
  """
  Manages challenge requests.
  """
  permission_classes = (ChallengePermission,)

  def get(self, request, format=None):
    """
    Gets all challenges
    """
    challenges = Challenge.objects.all()

    if request.user.is_staff:
      serialized_challenges = AdminChallengeSerializer(challenges, many=True, context={'request': request})
    else:
      serialized_challenges = ChallengeSerializer(challenges, many=True, context={'request': request})
    return Response({
      'challenges': serialized_challenges.data,
    })

  def post(self, request, format=None):
    """
    Create a new challenge
    """
    if 'challenge' not in request.data or not request.data['challenge']:
      return error_response('Challenge not given')

    challenge_data = request.data['challenge']
    if 'category' not in challenge_data or not challenge_data['category']:
      return error_response('Challenge category not given', errorfields={'category': True})
    if 'title' not in challenge_data or not challenge_data['title']:
      return error_response('Challenge title not given', errorfields={'title': True})
    if 'points' not in challenge_data or not challenge_data['points']:
      return error_response('Challenge points not given', errorfields={'points': True})
    if 'description' not in challenge_data or not challenge_data['description']:
      return error_response('Challenge description not given', errorfields={'description': True})
    if 'flag' not in challenge_data or not challenge_data['flag']:
      return error_response('Challenge flag not given', errorfields={'flag': True})

    try:
      category_id = int(challenge_data['category'])
    except ValueError:
      return error_response('Challenge not found', errorfields={'category': True})

    try:
      category = Category.objects.get(id=category_id)
    except ObjectDoesNotExist:
      return error_response('Challenge not found', errorfields={'category': True})

    try:
      points = int(challenge_data['points'])
    except ValueError:
      return error_response('Invalid challenge points', errorfields={'points': True})

    title = str(challenge_data['title'])
    if len(title) > 200:
      return error_response('Title greater than 200 characters', errorfields={'title': True})

    description = str(challenge_data['description'])
    if len(title) > 10000:
      return error_response('Description greater than 10000 characters', errorfields={'title': True})

    flag = str(challenge_data['flag'])
    if len(title) > 100:
      return error_response('Flag greater than 100 characters', errorfields={'title': True})

    challenge = Challenge.objects.create(category=category, title=title, points=points, description=description, flag=flag)
    if request.user.is_staff:
      serialized_challenge = AdminChallengeSerializer(challenge, many=False, context={'request': request})
    else:
      serialized_challenge = ChallengeSerializer(challenge, many=False, context={'request': request})
    return Response({
      'challenge': serialized_challenge.data,
    })


class ChallengeViewDetail(APIView):
  """
  Manages challenge by id requests.
  """
  permission_classes = (ChallengePermissionDetail,)

  def get(self, request, id, format=None):
    """
    Gets individual challenge via id
    """
    try:
      challenge = Challenge.objects.get(id=id)
    except ObjectDoesNotExist:
      return error_response('Challenge not found')

    if request.user.is_staff:
      serialized_challenge = AdminChallengeSerializer(challenge, many=False, context={'request': request})
    else:
      serialized_challenge = ChallengeSerializer(challenge, many=False, context={'request': request})
    return Response({
      'challenge': serialized_challenge.data,
    })

  def put(self, request, id, format=None):
    """
    Edits a challenge
    """
    try:
      challenge = Challenge.objects.get(id=id)
    except ObjectDoesNotExist:
      return error_response('Challenge not found')

    if 'challenge' not in request.data or not request.data['challenge']:
      return error_response('Challenge not given')

    challenge_data = request.data['challenge']
    if 'title' not in challenge_data or not challenge_data['title']:
      return error_response('Challenge title not given', errorfields={'title': True})
    if 'points' not in challenge_data or not challenge_data['points']:
      return error_response('Challenge points not given', errorfields={'points': True})
    if 'description' not in challenge_data or not challenge_data['description']:
      return error_response('Challenge description not given', errorfields={'description': True})
    if 'flag' not in challenge_data or not challenge_data['flag']:
      return error_response('Challenge flag not given', errorfields={'flag': True})

    try:
      points = int(challenge_data['points'])
    except ValueError:
      return error_response('Invalid challenge points', errorfields={'points': True})

    title = str(challenge_data['title'])
    if len(title) > 200:
      return error_response('Title greater than 200 characters', errorfields={'title': True})

    description = str(challenge_data['description'])
    if len(description) > 10000:
      return error_response('Description greater than 10000 characters', errorfields={'description': True})

    flag = str(challenge_data['flag'])
    if len(flag) > 100:
      return error_response('Flag greater than 100 characters', errorfields={'flag': True})

    challenge.title = title
    challenge.points = points
    challenge.description = description
    challenge.flag = flag

    challenge.save()
    if request.user.is_staff:
      serialized_challenge = AdminChallengeSerializer(challenge, many=False, context={'request': request})
    else:
      serialized_challenge = ChallengeSerializer(challenge, many=False, context={'request': request})
    return Response({
      'challenge': serialized_challenge.data,
    })

  def delete(self, request, id, format=None):
    """
    Deletes a challenge
    """
    try:
      challenge = Challenge.objects.get(id=id)
    except ObjectDoesNotExist:
      return error_response('Challenge not found')
    challenge.delete()
    return Response({})


from rest_framework.views import APIView
from rest_framework.response import Response
from edctf.api.models import Challengeboard, Category, Challenge
from edctf.api.permissions import ChallengeboardPermission, ChallengeboardPermissionDetail
from edctf.api.serializers import ChallengeboardSerializer, CategorySerializer, ChallengeSerializer
from edctf.api.serializers.admin import ChallengeboardSerializer as AdminChallengeboardSerializer
from edctf.api.serializers.admin import CategorySerializer as AdminCategorySerializer
from edctf.api.serializers.admin import ChallengeSerializer as AdminChallengeSerializer
from response import error_response


class ChallengeboardView(APIView):
  """
  Manages challengeboard requests
  """
  permission_classes = (ChallengeboardPermission,)

  def get(self, request, id=None, format=None):
    """
    Gets all challengeboards
    """
    challengeboards = Challengeboard.objects.all()

    if request.user.is_staff:
      serialized_challengeboards = AdminChallengeboardSerializer(challengeboards, many=True, context={'request': request})
    else:
      serialized_challengeboards = ChallengeboardSerializer(challengeboards, many=True, context={'request': request})
    return Response({
        'challengeboards': serialized_challengeboards.data,
    })



class ChallengeboardViewDetail(APIView):
  """
  Manages challengeboards by id requests.
  """
  permission_classes = (ChallengeboardPermissionDetail,)

  def get(self, request, id, format=None):
    """
    Gets all challengeboard by id
    """
    try:
      challengeboard = Challengeboard.objects.get(id=id)
    except ObjectDoesNotExist:
      return error_response('Challengeboard not found')

    categories = challengeboard.categories
    challenges = []
    for cat in categories:
      challenges += categories.challenges

    if request.user.is_staff:
      serialized_challengeboards = AdminChallengeboardSerializer(challengeboard, many=True, context={'request': request})
      serialized_categories = AdminCategorySerializer(categories, many=True, context={'request': request})
      serialized_challenges = AdminChallengeSerializer(challenges, many=True, context={'request': request})
    else:
      serialized_challengeboards = ChallengeboardSerializer(challengeboard, many=True, context={'request': request})
      serialized_categories = CategorySerializer(categories, many=True, context={'request': request})
      serialized_challenges = ChallengeSerializer(challenges, many=True, context={'request': request})
    return Response({
        'challengeboards': serialized_challengeboards.data,
        'categories': serialized_categories.data,
        'challenges': serialized_challenges.data,
    })

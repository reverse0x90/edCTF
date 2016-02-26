from rest_framework.views import APIView
from rest_framework.response import Response
from edctf.api.models import Challengeboard, Category, Challenge
from edctf.api.permissions import ChallengeboardPermission
from edctf.api.serializers import ChallengeboardSerializer, CategorySerializer, ChallengeSerializer
from edctf.api.serializers.admin import ChallengeSerializer as AdminChallengeSerializer


class ChallengeboardView(APIView):
  """
  Manages challengeboard requests
  """
  permission_classes = (ChallengeboardPermission,)

  def get(self, request, id=None, format=None):
    """
    Gets all challengeboards or gets one challengeboard via
    challengeboards/:id.
    """
    # If challengeboard id was requested, return that challengeboard
    # else return list of all challengeboards in the database.
    if id:
      # Retrieve and serialize the requested challengeboard data.
      challengeboards = Challengeboard.objects.filter(id=id)
      challengeboards_serializer = ChallengeboardSerializer(challengeboards, many=True, context={'request': request})

      # Retrieve and serialize the categories in the challengeboard.
      categories = Category.objects.filter(challengeboard=challengeboards.first())
      categories_serializer = CategorySerializer(categories, many=True, context={'request': request})

      # Retrieve and serialize the challenges in each category.
      challenges = []
      for cat in categories:
        challenges += Challenge.objects.filter(category=cat)

      if request.user.is_staff:
        challenges_serializer = AdminChallengeSerializer(challenges, many=True, context={'request': request})
      else:
        challenges_serializer = ChallengeSerializer(challenges, many=True, context={'request': request})

      # Return the serialized data.
      return Response({
          'challengeboards': challengeboards_serializer.data,
          'categories': categories_serializer.data,
          'challenges': challenges_serializer.data,
      })
    else:
      # Retrieve and serialize the requested challengeboard data.
      challengeboards = Challengeboard.objects.all()
      serializer = ChallengeboardSerializer(challengeboards, many=True, context={'request': request})

      # Return the serialized data.
      return Response({
          'challengeboards': serializer.data,
      })

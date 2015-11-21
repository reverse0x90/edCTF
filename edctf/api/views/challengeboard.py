from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from edctf.api.models import challengeboard, category, challenge
from edctf.api.serializers import challengeboardSerializer, categorySerializer, challengeSerializer


class challengeboardView(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request, id=None, format=None):
        """
        Get all challengeboards
        or get by id via challengeboards/:id
        """
        if id:
            challengeboards = challengeboard.objects.filter(id=id)
            challengeboards_serializer = challengeboardSerializer(challengeboards, many=True, context={'request': request})

            categories = category.objects.filter(challengeboard=challengeboards[0])
            categories_serializer = categorySerializer(categories, many=True, context={'request': request})

            challenges = []
            for cat in categories:
                challenges += challenge.objects.filter(category=cat)
            challenges_serializer = challengeSerializer(challenges, many=True, context={'request': request})

            return Response({
                "challengeboards": challengeboards_serializer.data,
                "categories": categories_serializer.data,
                "challenges": challenges_serializer.data,
            })
        else:
            challengeboards = challengeboard.objects.all()
            serializer = challengeboardSerializer(challengeboards, many=True, context={'request': request})
            return Response({
                "challengeboards": serializer.data,
            })

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from edctf.api.models import team
from edctf.api.serializers import teamSerializer


class teamView(APIView):
    permission_classes = (AllowAny,)
    def get(self, request, id=None, format=None):
        """
        Get all teams
        or get by id via teams/:id
        """
        if id:
            teams = team.objects.filter(id=id)
        else:
            teams = team.objects.all()
        teams_serializer = teamSerializer(teams, many=True, context={'request': request})
        return Response({
            "teams": teams_serializer.data,
        })

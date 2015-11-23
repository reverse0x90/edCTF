from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework import status
from edctf.api.models import team
from edctf.api.serializers import teamSerializer
import json


class teamView(APIView):
    permission_classes = (AllowAny,)
    
    def get(self, request, id=None, format=None):
        """
        Gets all teams or gets by id via /teams/:id
        """
        if id:
            teams = team.objects.filter(id=id)
        else:
            teams = team.objects.all()
        teams_serializer = teamSerializer(teams, many=True, context={'request': request})
        return Response({
            "teams": teams_serializer.data,
        })

    def post(self, request, *args, **kwargs):
        """
        Registers a new team
        """
        test = {
            'test': json.loads(request.body)
        }
        
        return Response(test,status=status.HTTP_403_FORBIDDEN)

    def put(self, request, *args, **kwargs):
        """
        Edit team profile
        """
        return Response(status=status.HTTP_403_FORBIDDEN)

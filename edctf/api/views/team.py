from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework import status
from edctf.api.models import team, ctf
from edctf.api.serializers import teamSerializer
import json


class teamView(APIView):
    permission_classes = (AllowAny,)
    
    def form_response(self, isauthenticated, username='', email='', teamid='', error='', errorfields={}):
        data = {
            'isauthenticated': isauthenticated,
        }
        if error:
            data['error'] = error
            data['errorfields'] = errorfields
        else:
            data['username'] = username
            data['email'] = email
            data['team'] = teamid
        return Response(data)

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
        if request.user.is_authenticated():
            logout(request)
            #return Response(status=status.HTTP_401_UNAUTHORIZED)
        
        live_ctf = ctf.objects.filter(live=True)
        if len(live_ctf) < 1:
            return Response(status=status.HTTP_403_FORBIDDEN)
        scoreboard = live_ctf[0].scoreboard.all()[0]

        team_data = json.loads(request.body)
        if not ('username' in team_data and 'teamname' in team_data and 'email' in team_data and 'password' in team_data):
            return Response(status=status.HTTP_400_BAD_REQUEST)

        teamname = team_data['teamname']
        email = team_data['email']
        username = team_data['username']
        password = team_data['password']

        check = User.objects.filter(username=username)
        if len(check):
            return self.form_response(False, error='Username is taken', errorfields={'username':True})
        check = User.objects.filter(email=email)
        if len(check):
            return self.form_response(False, error='Email is taken', errorfields={'email': True})
        check = team.objects.filter(teamname=teamname)
        if len(check):
            return self.form_response(False, error='Team name is taken', errorfields={'teamname': True})
        
        new_user = User.objects.create_user(username, email, password)
        new_team = team.objects.create(scoreboard=scoreboard, teamname=teamname,user=new_user)
        new_user.save()
        new_team.save()

        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
                return self.form_response(True, username=username, email=email, teamid=new_team.id)
            return self.form_response(False, error='User account is disabled')
        return self.form_response(False, error='Server error')

    def put(self, request, *args, **kwargs):
        """
        Edit team profile
        """
        return Response(status=status.HTTP_403_FORBIDDEN)

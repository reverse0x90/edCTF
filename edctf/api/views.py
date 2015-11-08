from django.shortcuts import render_to_response
from django.shortcuts import RequestContext
from django.contrib.auth import authenticate, login, logout

# Import models
from django.db import models
from django.contrib.auth.models import *
from edctf.api.models import *

#REST API
from django.http import Http404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework import status
from edctf.api.serializers import *

# Static pages
def home(request):
  """
  Send requests to / to the ember.js clientside app
  """
  return render_to_response('index.html', {}, RequestContext(request))

def robots(request):
  """
  Allows access to /robots.txt
  """
  return render(request, 'robots.txt', {},  content_type="text/plain")

def crossdomain(request):
  """
  Allows access to /crossdomain.xml
  """
  return render(request, 'crossdomain.xml', {},  content_type="application/xml")

# Create your views here.
class sessionView(APIView):
    """
    Manages sessions
    """
    permission_classes = (AllowAny,)
    error_messages = {
        'invalid': "Invalid username or password",
        'disabled': "Sorry, this account is suspended",
    }

    def send_error_response(self, message_key):
        data = {
            'success': False,
            'message': self.error_messages[message_key],
            'team': None,
        }
        return Response(data)

    #'''
    def get(self, request, *args, **kwargs):
        # Get the current user
        if request.user.is_authenticated():
            return Response({
                'team': request.user.teams.id,
            })
        return Response({'team': None})

    def post(self, request, *args, **kwargs):
        if request.user.is_authenticated():
            return Response(status=status.HTTP_401_UNAUTHORIZED)
        # Login
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
                return Response({
                    'success': True,
                    'team': request.user.teams.id,
                })
            return self.send_error_response('disabled')
        return self.send_error_response('invalid')

    def delete(self, request, *args, **kwargs):
        # Logout
        if request.user.is_authenticated():
            logout(request)
            return Response(status=status.HTTP_204_NO_CONTENT)
        return Response(status=status.HTTP_401_UNAUTHORIZED)

class ctfView(APIView):
    """
    List all ctfs
    or list by id via ctfs/:id
    or list all live ctfs via GET parameter, i.e. live=true
    """
    permission_classes = (AllowAny,)
    def get(self, request, id=None, format=None):
        if id:
            ctfs = ctf.objects.all().filter(id=id)
        else:
            if 'live' in request.query_params:
                if request.query_params['live'] == 'true':
                    ctfs = ctf.objects.all().filter(live=True)
                else:
                    ctfs = ctf.objects.all().filter(live=False)
            else:
                ctfs = ctf.objects.all()
        serializer = ctfSerializer(ctfs, many=True, context={'request': request})
        return Response({
            "ctfs": serializer.data,
        })

class challengeboardView(APIView):
    """
    List all challengeboards
    or list by id via challengeboards/:id
    """
    permission_classes = (AllowAny,)
    #permission_classes = (IsAuthenticated,)
    def get(self, request, id=None, format=None):
        if id:
            challengeboards = challengeboard.objects.all().filter(id=id)
            challengeboards_serializer = challengeboardSerializer(challengeboards, many=True, context={'request': request})

            categories = category.objects.all().filter(challengeboard=challengeboards[0])
            categories_serializer = categorySerializer(categories, many=True, context={'request': request})

            challenges = []
            for cat in categories:
                challenges += challenge.objects.all().filter(category=cat)
            challenges_serializer = challengesSerializer(challenges, many=True, context={'request': request})

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

class scoreboardView(APIView):
    """
    List all scoreboards
    or list by id via scoreboards/:id
    """
    permission_classes = (AllowAny,)
    def get(self, request, id=None, format=None):
        if id:
            scoreboards = scoreboard.objects.all().filter(id=id)
            scoreboards_serializer = scoreboardSerializer(scoreboards, many=True, context={'request': request})
            
            scoreboards_serializer.data[0]['topteamsdata'] = {
                "x": 'x',
                "columns": [
                    ['x', '2013-01-01', '2013-01-02', '2013-01-03',],
                    ["team0", 0, 299, 1000],
                    ["team1", 0, 732, 975],
                    ["team2", 0, 929, 953],
                    ["team3", 0, 670, 933],
                    ["team4", 0, 362, 933],
                    ["team5", 0, 490, 918],
                    ["team6", 0, 722, 893],
                    ["team7", 0, 632, 876],
                    ["team8", 0, 274, 875],
                    ["team9", 0, 768, 872],
                ],
            }

            teams = team.objects.order_by('points').filter(scoreboard=scoreboards[0])
            teams_serializer = teamSerializer(teams, many=True, context={'request': request})
            for pos,t in enumerate(teams_serializer.data):
                t['position'] = pos+1

            return Response({
                "scoreboards": scoreboards_serializer.data,
                "teams": teams_serializer.data,
            })

        else:
            scoreboards = scoreboard.objects.all()
            scoreboards_serializer = scoreboardSerializer(scoreboards, many=True, context={'request': request})
            return Response({
                "scoreboards": scoreboards_serializer.data,
            })

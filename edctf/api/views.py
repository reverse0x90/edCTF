from django.shortcuts import render_to_response
from django.shortcuts import RequestContext
from django.contrib.auth import authenticate, login, logout
from django.views.decorators.csrf import csrf_exempt

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


def check_flag(challenge, flag):
    '''
    Checks a given flag with a challenge.
    '''
    # Allow regex in the future
    return challenge.flag == flag;

def update_solved(user, challenge):
    '''
    Gives points to a given user
    '''
    points = user.points
    user.solved.add(challenge)
    user.points = points + challenge.points
    user.save()
    challenge.save()



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
        'invalid': 'Invalid username or password',
        'disabled': 'This account is suspended',
        'isloggedin': 'Already logged in',
    }

    def send_error_response(self, message_key):
        data = {
            'success': False,
            'message': self.error_messages[message_key],
            'team': None,
        }
        return Response(data, status=status.HTTP_401_UNAUTHORIZED)

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated():
            try:
                return Response({
                    'success': True,
                    'team': request.user.teams.id,
                })
            # Temporary: Django admin doesnt have a team..
            except:
                return Response({
                    'success': True,
                    'team': None,
                })
        return Response({
            'success': False,
            'team': None,
        })

    def post(self, request, *args, **kwargs):
        if request.user.is_authenticated():
            logout(request)
        #    return self.send_error_response('isloggedin')
        
        # Login
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
                try:
                    return Response({
                        'success': True,
                        'team': user.teams.id,
                    })
                # Temporary: Django admin doesnt have a team..
                except:
                    return Response({
                        'success': True,
                        'team': None,
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
    permission_classes = (AllowAny,)
    def get(self, request, id=None, format=None):
        """
        Get all ctfs
        or get by id via ctfs/:id
        or get all live ctfs via GET parameter, i.e. live=true
        """
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
    permission_classes = (IsAuthenticated,)
    def get(self, request, id=None, format=None):
        """
        Get all challengeboards
        or get by id via challengeboards/:id
        """
        if id:
            challengeboards = challengeboard.objects.all().filter(id=id)
            challengeboards_serializer = challengeboardSerializer(challengeboards, many=True, context={'request': request})

            categories = category.objects.all().filter(challengeboard=challengeboards[0])
            categories_serializer = categorySerializer(categories, many=True, context={'request': request})

            challenges = []
            for cat in categories:
                challenges += challenge.objects.all().filter(category=cat)
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

class challengeView(APIView):
    permission_classes = (IsAuthenticated,)
    def get(self, request, id=None, format=None):
        """
        Get all challenge
        or get by id via challenge/:id
        """
        if id:
            challenges = challenges.objects.all().filter(id=id)
        else:
            challenge = challenge.objects.all()
        challenge_serializer = challengeSerializer(challenges, many=True, context={'request': request})
        return Response({
            "challenges": challenge_serializer.data,
        })
    def post(self, request, id=None, format=None):
        '''
        Submit a flag for a challenge
        '''
        if id:
            try:
                _challenge = challenge.objects.get(id=id)
            except:
                return Response({
                    "success": False
                }, status=status.HTTP_404_NOT_FOUND)
            
            flag = request.POST.get('flag')
            if not flag:
                return Response({
                    "success": False
                }, status=status.HTTP_401_UNAUTHORIZED)

            if check_flag(_challenge, flag):
                try:
                    _team = team.objects.get(id=request.user.teams.id)
                except:
                    return Response({
                        "success": False
                    }, status=status.HTTP_401_UNAUTHORIZED)
                update_solved(_team, _challenge)
                return Response({
                    "success": True
                })
            else:
                return Response({
                    "success": False
                })
        else:
            return Response(status=status.HTTP_401_UNAUTHORIZED)

class scoreboardView(APIView):
    permission_classes = (AllowAny,)
    def get(self, request, id=None, format=None):
        """
        Get all scoreboards
        or get by id via scoreboards/:id
        """
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

class teamView(APIView):
    permission_classes = (AllowAny,)
    def get(self, request, id=None, format=None):
        """
        Get all teams
        or get by id via teams/:id
        """
        if id:
            teams = team.objects.all().filter(id=id)
        else:
            teams = team.objects.all()
        teams_serializer = teamSerializer(teams, many=True, context={'request': request})
        return Response({
            "teams": teams_serializer.data,
        })

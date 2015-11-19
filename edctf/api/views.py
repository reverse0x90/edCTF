from django.shortcuts import render_to_response
from django.shortcuts import RequestContext
from django.contrib.auth import authenticate, login, logout
from django.views.decorators.csrf import csrf_exempt
from django.core.exceptions import ObjectDoesNotExist
import time

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


def check_flag(team, challenge, flag):
    '''
    Checks a given flag with a challenge.
    '''
    
    res = team.solved.filter(id=challenge.id)
    
    # if not solved, do flag check
    if not res:
        # Allow regex in the future
        correct1 = challenge.flag == flag
        correct2 = challenge.flag == str('null{'+flag+'}')
        correct = correct1 or correct2
        if correct:
            team.correct_flags = team.correct_flags + 1
            team.save()
            return True
        else:
            team.wrong_flags = team.wrong_flags + 1
            team.save()
            return False
    # already solved
    else:
        team.wrong_flags = team.wrong_flags + 1
        team.save()
        return False

def check_flag2(challenge, flag):
    '''
    Checks a given flag with a challenge, doesnt update db, doesnt need team
    '''

    # Allow regex in the future
    correct1 = challenge.flag == flag
    correct2 = challenge.flag == str('null{'+flag+'}')
    correct = correct1 or correct2
    if correct:
        return True
    else:
        return False

def update_solved(team, challenge):
    '''
    Gives points to a given user
    '''
    #team.solved.add(challenge)
    timestamp = challengeTimestamp.objects.create(team=team, challenge=challenge)
    timestamp.save()

    team.points = team.points + challenge.points
    team.last_timestamp = timestamp.created
    team.save()
    challenge.save()

def get_topteamsdata(teams):
    data = {}
    data['xs'] = {}
    data['type'] = 'step'
    data['columns'] = []

    current_time = int(time.time())
    #start = current_time - (60*60*12) # only show past 12 hours
    delta_initial_point_timestamp = 60*5

    points = initial_points = 0
    for position,team in enumerate(teams):
        time_data = [str(position)]
        point_data = [team.teamname]
        
        challengeTimestamps = team.challengeTimestamps.order_by('created')
        for i,challengeTimestamp in enumerate(challengeTimestamps):
            timestamp = int(time.mktime(challengeTimestamp.created.timetuple()))
            if i == 0:
                time_data.append(timestamp-delta_initial_point_timestamp)
                point_data.append(points)
            points = points + challengeTimestamp.challenge.points
            #if timestamp < start:
            #    continue
            

            time_data.append(timestamp)
            point_data.append(points)
        time_data.append(current_time)
        point_data.append(team.points)
        data['xs'][team.teamname] = str(position)
        data['columns'].append(time_data)
        data['columns'].append(point_data)
        points = initial_points
    return data

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
            ctfs = ctf.objects.filter(id=id)
        else:
            if 'live' in request.query_params:
                if request.query_params['live'] == 'true':
                    ctfs = ctf.objects.filter(live=True)
                else:
                    ctfs = ctf.objects.filter(live=False)
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

class challengeView(APIView):
    permission_classes = (IsAuthenticated,)
    def get(self, request, id=None, format=None):
        """
        Get all challenge
        or get by id via challenge/:id
        """
        if id:
            challenges = challenge.objects.filter(id=id)
        else:
            challenges = challenge.objects.all()
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

            _team = request.user.teams
            #if check_flag(_team,_challenge, flag):
            if check_flag(_challenge, flag):
                #update_solved(_team, _challenge)
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
            # Set scoreboard object
            scoreboards = scoreboard.objects.filter(id=id)
            scoreboards_serializer = scoreboardSerializer(scoreboards, many=True, context={'request': request})
            
            # Set teams from scoreboard
            teams = team.objects.filter(scoreboard=scoreboards[0]).order_by('-points','-last_timestamp')
            teams_serializer = teamSerializer(teams, many=True, context={'request': request})
            for pos,t in enumerate(teams_serializer.data):
                t['position'] = pos+1

            # Create top teams c3 data
            scoreboards_serializer.data[0]['topteamsdata'] = get_topteamsdata(teams[:scoreboards[0].numtopteams])

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
            teams = team.objects.filter(id=id)
        else:
            teams = team.objects.all()
        teams_serializer = teamSerializer(teams, many=True, context={'request': request})
        return Response({
            "teams": teams_serializer.data,
        })

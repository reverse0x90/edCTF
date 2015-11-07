from django.shortcuts import render_to_response
from django.shortcuts import RequestContext
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import authentication, permissions, status

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

#
from rest_framework.decorators import api_view
from edctf.api import temp
@api_view(['GET'])
def ctf(request, id=None):
    if request.method == 'GET':
        ctfs = temp.ctfs
        if id:
            if id.isdigit():
                # return where id=path
                id = int(id)
                ctf = [c for c in ctfs if c['id']==id]
                if ctf:
                    return Response({'ctfs': ctf[0]})
                else:
                    return Response(status=status.HTTP_404_NOT_FOUND)
            else:
                # given path is not excepted
                return Response(status=status.HTTP_400_BAD_REQUEST)
        if "live" in request.query_params:
            if request.query_params["live"].lower() == "true":
                # return where live=True
                return Response({'ctfs': ctfs[:1]})
            else:
                # return where live=false
                return Response({'ctfs': ctfs[1:]})
        # return all ctfs
        return Response(ctfs)

@api_view(['GET'])
def challengeboard(request, id=None):
    if request.method == 'GET':
        challengeboard = temp.challengeboard
        if id:
            if id.isdigit():
                # return where id=id
                id = int(id)
                if id == 1:
                    return Response(challengeboard)
                else:
                    return Response(status=status.HTTP_404_NOT_FOUND)
            else:
                # given path is not excepted
                return Response(status=status.HTTP_400_BAD_REQUEST)
        return Response(status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
def scoreboard(request, id=None):
    if request.method == 'GET':
        scoreboard = temp.scoreboard
        if id:
            if id.isdigit():
                # return where id=id
                id = int(id)
                if id == 1:
                    return Response(scoreboard)
                else:
                    return Response(status=status.HTTP_404_NOT_FOUND)
            else:
                # given path is not excepted
                return Response(status=status.HTTP_400_BAD_REQUEST)
        return Response(status=status.HTTP_400_BAD_REQUEST)

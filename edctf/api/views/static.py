from django.shortcuts import render, render_to_response
from django.shortcuts import RequestContext


def home(request):
  """
  Sends requests to / to the ember.js clientside app
  """
  return render(request, 'index.html', {},  content_type="text/html")


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

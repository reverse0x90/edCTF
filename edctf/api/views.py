from django.shortcuts import *

# Create your views here.
def home(request):
  """
  Send requests to / to the ember.js clientside app
  """
  
  return render_to_response('index.html',
                {}, RequestContext(request))

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

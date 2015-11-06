from django.shortcuts import *

# Create your views here.
def home(request):
  """
  Send requests to / to the ember.js clientside app  """
  
  return render_to_response('index.html',
                {}, RequestContext(request))
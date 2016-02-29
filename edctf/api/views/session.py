from django.conf import settings
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
from edctf.api.models import Ctf
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from ratelimit.decorators import ratelimit
from edctf.api.permissions import SessionPermission


class SessionView(APIView):
  """
  Manages server side user sessions
  """
  permission_classes = (SessionPermission,)

  def form_response(self, isauthenticated, user=None, username='', error=''):
    """
    Returns the login form response.
    """
    # Create return data dictionary.
    data = {
      'isauthenticated': isauthenticated,
    }
    # If error during login, return the error else return login data.
    if error:
      data['error'] = error
    
    if user:
      data['username'] = username or user.username
      data['email'] = user.email
      data['isadmin'] = user.is_superuser
      try:
        data['team'] = user.team.id
      except:
        data['team'] = None
    return Response(data)

  def get(self, request, *args, **kwargs):
    """
    Returns authentication data.
    """
    # If user is authenticated, return authentication data else
    # return a "not authenticated" error.
    if request.user.is_authenticated():
      return self.form_response(True, user=request.user)
    return self.form_response(False, error='Not authenticated')

  @ratelimit(key='ip', rate='15/m')
  def post(self, request, *args, **kwargs):
    """
    Uses provided json data to authenticate and login a user.
    """
    was_limited = getattr(request, 'limited', False)
    if was_limited:
      return self.form_response(False, error='Too many login attempts')
    
    # If user is already authenticated, logout the user.
    if request.user.is_authenticated():
      logout(request)

    # Serialize the provided login json data to a python object.
    login_data = request.data

    # Sanity check the json data to make sure all required parameters
    # are included.
    if not ('username' in login_data and 'password' in login_data):
      return self.form_response(False, error='Invalid parameters')

    # Authenticate the user.
    username = login_data['username']
    password = login_data['password']

    try:
      User.objects.get(username=username)
      ctfuser = False
    except ObjectDoesNotExist:
      ctfuser = True

    if ctfuser:
      enc_username = ctf_encode(username)
      if not enc_username:
        return self.form_response(False, error='No online CTF, cannot login')
      user = authenticate(username=enc_username, password=password)
      if user is not None and user.is_active:
        login(request, user)
        return self.form_response(True, user=request.user, username=username)
    else:
      user = authenticate(username=username, password=password)
      if user is not None and user.is_active:
        login(request, user)
        return self.form_response(True, user=request.user)
    return self.form_response(False, error='Invalid username or password')

  def delete(self, request, *args, **kwargs):
    """
    Logout the user
    """
    # If user is authenticated, logout the user else return a 401
    # error message.
    if request.user.is_authenticated():
      logout(request)
      return Response(status=status.HTTP_204_NO_CONTENT)
    return Response(status=status.HTTP_401_UNAUTHORIZED)

def ctf_encode(plaintext):
  """
  Encodes a given plaintext with the online CTF as salt
  """
  try:
    ctf = Ctf.objects.get(online=True)
  except ObjectDoesNotExist:
    return False
  salt = '{id}'.format(id=ctf.id)
  return salt+'_'+plaintext

def ctf_decode(salted_ciphertext):
  """
  Decodes given ciphertext, returns tuple of (salt, plaintext)
  """
  if '_' not in salted_ciphertext:
    return False
  ciphertext = salted_ciphertext.split('_')
  if len(ciphertext) < 2:
    return False
  salt, ciphertext = ciphertext[0], ''.join(ciphertext[1:])
  return salt, ciphertext

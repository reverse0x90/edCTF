from django.conf import settings
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth import get_user_model
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

  def form_response(self, isauthenticated, user=None, error=''):
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
      data['username'] = user.username
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

    login_data = request.data
    if not ('username' in login_data and 'password' in login_data):
      return self.form_response(False, error='Invalid parameters')

    # Authenticate the user.
    username = login_data['username']
    password = login_data['password']

    User = get_user_model()
    try:
      User.objects.get(enc_username=username)
      ctfuser = False
    except ObjectDoesNotExist:
      ctfuser = True

    if ctfuser:
      try:
        ctf = Ctf.objects.get(online=True)
      except:
        return self.form_response(False, error='No online CTF, cannot login')

      enc_username = User.objects.encrypt_username(username, ctf)
      user = authenticate(enc_username=enc_username, password=password)
      if user is not None and user.is_active:
        login(request, user)
        return self.form_response(True, user=request.user)
    else:
      user = authenticate(enc_username=username, password=password)
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

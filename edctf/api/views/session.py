from django.contrib.auth import authenticate, login, logout
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
        data['team'] = user.teams.id
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
      return Response(status=status.HTTP_400_BAD_REQUEST)

    # Authenticate the user.
    username = login_data['username']
    password = login_data['password']
    user = authenticate(username=username, password=password)

    # If user authentication was sucessful, login the user else
    # return an error message.
    if user is not None:
      if user.is_active:
        login(request, user)
        return self.form_response(True, user=request.user)
      return self.form_response(False, error='Acount disabled')
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

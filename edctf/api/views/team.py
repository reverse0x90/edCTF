from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.core.validators import EmailValidator
from ratelimit.decorators import ratelimit
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from response import error_response
from edctf.api.models import Team, Ctf
from edctf.api.permissions import TeamPermission
from edctf.api.serializers import TeamSerializer
from edctf.api.validators import validate_no_html, validate_no_xss
from edctf.api.views import ctf_encode


class TeamView(APIView):
  """
  Manages team requests.
  """
  permission_classes = (TeamPermission,)

  def form_response(self, isauthenticated, user=None, username='', error='', errorfields={}):
    """
    Returns the registration form response.
    """
    # Create return data dictionary.
    data = {
        'isauthenticated': isauthenticated,
    }
    # If error during registration, return the error else return
    # the registration data.
    if error:
      data['error'] = error
      data['errorfields'] = errorfields
    if user:
      data['username'] = username or user.username
      data['email'] = user.email
      data['isadmin'] = user.is_superuser
      try:
        data['team'] = user.teams.id
      except:
        data['team'] = None
    return Response(data)

  def get(self, request, id=None, format=None):
    """
    Gets all teams or gets an individual team via /teams/:id.
    """
    # If a specific team is requested, return that team
    # else return all the teams.
    if id:
      teams = Team.objects.filter(id=id)
    else:
      teams = Team.objects.all()

    # Serialize team object and return the serialized data.
    teams_serializer = TeamSerializer(teams, many=True, context={'request': request})

    return Response({
      'teams': teams_serializer.data,
    })

  @ratelimit(key='ip', rate='5/m')
  def post(self, request, *args, **kwargs):
    """
    Registers a new team to online ctf
    """
    # If user is already authenticated, logout the user.
    was_limited = getattr(request, 'limited', False)
    if was_limited:
      return self.form_response(False, error='Too many recent registrations')
    
    if request.user.is_authenticated():
      logout(request)

    # Get the current online ctf (aka the active ctf).
    try:
      ctf = Ctf.objects.get(online=True)
    except:
      return self.form_response(False, error='No online CTF, cannot register')

    # Get the scoreboard object associated with the online ctf.
    scoreboard = ctf.scoreboard
    teams = scoreboard.teams

    # Save provided registration json data.
    team_data = request.data

    if not ('username' in team_data and 'teamname' in team_data and 'email' in team_data and 'password' in team_data):
      return self.form_response(False, error='Invalid parameters')

    username = team_data['username']
    teamname = team_data['teamname']
    email = team_data['email']
    password = team_data['password']
    enc_username = ctf_encode(team_data['username'])
    if not enc_username:
      return self.form_response(False, error='No online CTF, cannot register')

    check = teams.filter(email__iexact=email)
    if len(check):
      return self.form_response(False, error='Email is taken', errorfields={'email': True})
    else:
      try:
        EmailValidator(email)
      except ValidationError as e:
        return self.form_response(False, error=e.message, errorfields={'email': True})

    check = teams.filter(teamname__iexact=teamname)
    if len(check):
      return self.form_response(False, error='Team name is taken', errorfields={'teamname': True})

    check = User.objects.filter(username__iexact=enc_username)
    if len(check):
      return self.form_response(False, error='Username is taken', errorfields={'username': True})

    # check for username length, since django default is 30
    if len(username) > 25:
      return self.form_response(False, error='Username too long, 25 characters max')

    # Create temp user to validate input.
    temp_user = User(username=enc_username, email=email, password=password)
    try:
      temp_user.full_clean()
    except ValidationError as e:
      raise
      errordict = {}
      errorstr = ''
      # Get error keys
      for key in e.message_dict.keys():
        errordict[key] = True
        errorstr = str(e.message_dict[key][0])
        break
      return self.form_response(False, error=errorstr, errorfields=errordict)

    # Everything was good! Create the new user
    new_user = User.objects.create_user(enc_username, email, password)
    new_team = Team.objects.create(scoreboard=scoreboard, teamname=teamname, user=new_user, email=email)

    # Registration was successful! Now login the new user.
    user = authenticate(username=enc_username, password=password)
    if user is not None and user.is_active:
      login(request, user)
      return self.form_response(True, user, username=username)
    return self.form_response(False, error='Error with registration')

  def put(self, request, *args, **kwargs):
    """
    Edit team profile
    """
    # Return error message for now this feature will be supported
    # in a future release.
    return Response(status=status.HTTP_404_NOT_FOUND)

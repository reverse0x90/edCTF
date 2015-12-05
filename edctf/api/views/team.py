from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework import status
from edctf.api.models import team, ctf
from edctf.api.serializers import teamSerializer
from edctf.api.validators import *


class teamView(APIView):
  """
  Manages team requests.
  """
  permission_classes = (AllowAny,)

  def form_response(self, isauthenticated, username='', email='', teamid='', error='', errorfields={}):
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
    else:
        data['username'] = username
        data['email'] = email
        data['team'] = teamid
    return Response(data)

  def get(self, request, id=None, format=None):
    """
    Gets all teams or gets an individual team via /teams/:id.
    """
    # If a specific team is requested, return that team
    # else return all the teams.
    if id:
      teams = team.objects.filter(id=id)
    else:
      teams = team.objects.all()

    # Serialize team object and return the serialized data.
    teams_serializer = teamSerializer(teams, many=True, context={'request': request})
    return Response({
      "teams": teams_serializer.data,
    })

  def post(self, request, *args, **kwargs):
    """
    Registers a new team
    """
    # If user is already authenticated, logout the user.
    if request.user.is_authenticated():
      logout(request)

    # Get the current live ctf (aka the active ctf).
    live_ctf = ctf.objects.filter(live=True)

    # Sanity check currently there can only be one live ctf at a time.
    if len(live_ctf) < 1:
      return Response(status=status.HTTP_403_FORBIDDEN)

    # Get the scoreboard object associated with the live ctf.
    scoreboard = live_ctf[0].scoreboard.all()[0]

    # Save provided registration json data.
    team_data = request.data

    # Sanity check the json data to make sure all required parameters
    # are included.
    if not ('username' in team_data and 'teamname' in team_data and 'email' in team_data and 'password' in team_data):
      return Response(status=status.HTTP_400_BAD_REQUEST)

    # Assign registration data to local variables.
    teamname = team_data['teamname']
    email = team_data['email']
    username = team_data['username']
    password = team_data['password']

    # Make validation checks on user input.
    # This is a hacky way to make these validation checks, but it should work for now.
    # Check email field
    check = User.objects.filter(email=email)
    if len(check):
      return self.form_response(False, error='Email is taken', errorfields={'email': True})
    else:
      try:
        validate_no_html(email)
        validate_no_xss(email)
      except ValidationError as e:
        return self.form_response(False, error=e.message, errorfields={'email': True})

    # Check teamname field
    check = team.objects.filter(teamname=teamname)
    if len(check):
      return self.form_response(False, error='Team name is taken', errorfields={'teamname': True})
    else:
      try:
        validate_no_html(teamname)
        validate_no_xss(teamname)
      except ValidationError as e:
        return self.form_response(False, error=e.message, errorfields={'teamname': True})

    # Check teamname field
    check = User.objects.filter(username=username)
    if len(check):
      return self.form_response(False, error='Username is taken', errorfields={'username': True})
    else:
      try:
        validate_no_html(username)
        validate_no_xss(username)
      except ValidationError as e:
        return self.form_response(False, error=e.message, errorfields={'username': True})

    # Create temp user to validate input.
    temp_user = User(username=username, email=email, password=password)

    # Verify user model is valid, if it is add the user and team to the
    # database else return an error message.
    try:
      temp_user.full_clean()
    except ValidationError as e:
      errordict = {}
      errorstr = ""
      # Get error keys
      for key in e.message_dict.keys():
        errordict[key] = True
        errorstr = str(e.message_dict[key][0])
        break
      return self.form_response(False, error=errorstr, errorfields=errordict)

    # Everything was good! Create the new user
    new_user = User.objects.create_user(username, email, password)
    new_team = team.objects.create(scoreboard=scoreboard, teamname=teamname, user=new_user)

    # Registration was successful! Now login the new user.
    user = authenticate(username=username, password=password)
    if user is not None:
      if user.is_active:
        login(request, user)
        return self.form_response(True, username=username, email=email, teamid=new_team.id)
      return self.form_response(False, error='User account is disabled')
    return self.form_response(False, error='Server error')

  def put(self, request, *args, **kwargs):
    """
    Edit team profile
    """
    # Return error message for now this feature will be supported
    # in a future release.
    return Response(status=status.HTTP_403_FORBIDDEN)

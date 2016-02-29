from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError, ObjectDoesNotExist
from django.core.validators import EmailValidator
from ratelimit.decorators import ratelimit
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from response import error_response, registration_response
from edctf.api.models import Team, Ctf
from edctf.api.permissions import TeamPermission, TeamPermissionDetail
from edctf.api.serializers import TeamSerializer
from edctf.api.serializers.admin import TeamSerializer as AdminTeamSerializer
from edctf.api.validators import validate_no_html, validate_no_xss
from edctf.api.views import ctf_encode


class TeamView(APIView):
  """
  Manages team requests.
  """
  permission_classes = (TeamPermission,)

  def get(self, request, format=None):
    """
    Gets all teams
    """
    teams = Team.objects.all()
    if request.user.is_staff:
      serialized_teams = TeamSerializer(teams, many=True, context={'request': request})
    else:
      serialized_teams = AdminTeamSerializer(teams, many=True, context={'request': request})
    return Response({
      'teams': serialized_teams.data,
    })

  @ratelimit(key='ip', rate='5/m')
  def post(self, request, *args, **kwargs):
    """
    Registers a new team to online ctf
    """
    # If user is already authenticated, logout the user.
    was_limited = getattr(request, 'limited', False)
    if was_limited:
      return registration_response(False, error='Too many recent registrations')
    
    if request.user.is_authenticated():
      logout(request)

    # Get the current online ctf (aka the active ctf).
    try:
      ctf = Ctf.objects.get(online=True)
    except:
      return registration_response(False, error='No online CTF, cannot register')

    # Get the scoreboard object associated with the online ctf.
    scoreboard = ctf.scoreboard
    teams = scoreboard.teams

    team_data = request.data
    if not ('username' in team_data and 'teamname' in team_data and 'email' in team_data and 'password' in team_data):
      return registration_response(False, error='Invalid parameters')

    username = team_data['username']
    teamname = team_data['teamname']
    email = team_data['email']
    password = team_data['password']
    enc_username = ctf_encode(team_data['username'])
    if not enc_username:
      return registration_response(False, error='No online CTF, cannot register')

    check = teams.filter(email__iexact=email)
    if len(check):
      return registration_response(False, error='Email is taken', errorfields={'email': True})
    else:
      try:
        EmailValidator(email)
      except ValidationError as e:
        return registration_response(False, error=e.message, errorfields={'email': True})

    check = teams.filter(teamname__iexact=teamname)
    if len(check):
      return registration_response(False, error='Team name is taken', errorfields={'teamname': True})

    check = User.objects.filter(username__iexact=enc_username)
    if len(check):
      return registration_response(False, error='Username is taken', errorfields={'username': True})

    # check for username length, since django default is 30
    if len(username) > 25:
      return registration_response(False, error='Username too long, 25 characters max')

    # Create temp user to validate input.
    temp_user = User(username=enc_username, email=email, password=password)
    try:
      temp_user.full_clean()
    except ValidationError as e:
      errordict = {}
      errorstr = ''
      # Get error keys
      for key in e.message_dict.keys():
        errordict[key] = True
        errorstr = str(e.message_dict[key][0])
        break
      return registration_response(False, error=errorstr, errorfields=errordict)

    # Everything was good! Create the new user
    new_user = User.objects.create_user(enc_username, email, password)
    new_team = Team.objects.create(scoreboard=scoreboard, teamname=teamname, user=new_user, email=email)

    # Registration was successful! Now login the new user.
    user = authenticate(username=enc_username, password=password)
    if user is not None and user.is_active:
      login(request, user)
      return registration_response(True, user, username=username)
    return registration_response(False, error='Error with registration')


class TeamViewDetail(APIView):
  """
  Manages team requests.
  """
  permission_classes = (TeamPermissionDetail,)

  def get(self, request, id, format=None):
    """
    Gets team by id
    """
    try:
      team = Team.objects.get(id=id)
    except ObjectDoesNotExist:
      return error_response("Team not found")

    if request.user.is_staff:
      serialized_team = AdminTeamSerializer(team, many=False, context={'request': request})
    else:
      serialized_team = TeamSerializer(team, many=False, context={'request': request})
    return Response({
      'teams': serialized_team.data,
    })

  def put(self, request, id, format=None):
    """
    Edits a team
    """
    # modify to have separate edit if admin
    if request.user.team.id != id and not request.user.is_staff:
      return error_response("You do not have permission to edit this team")

    try:
      team = Teams.objects.get(id=id)
    except ObjectDoesNotExist:
      return error_response("Team not found")
    #user = request.user
    user = team.user

    team_data = request.data
    if not ('email' in team_data and 'password' in team_data):
      return registration_response(False, error='Invalid parameters')

    email = team_data['email']
    password = team_data['password']

    check = teams.filter(email__iexact=email)
    if len(check):
      return registration_response(False, error='Email is taken', errorfields={'email': True})
    else:
      try:
        EmailValidator(email)
      except ValidationError as e:
        return registration_response(False, error=e.message, errorfields={'email': True})

    # if non- admin do email-authentication tokens
    user.email = email
    user.password = password

    try:
      user.save()
      team.save()
    except IntegrityError:
      return error_response('Error modifying team')

    # change this to similar to session
    if request.user.is_staff:
      serialized_team = AdminTeamSerializer(team, many=False, context={'request': request})
    else:
      serialized_team = TeamSerializer(team, many=False, context={'request': request})
    return Response({
      'team': serialized_teamserialized_team.data,
    })

  def delete(self, request, id, format=None):
    """
    Deletes a team
    """
    try:
      team = Team.objects.get(id=id)
    except ObjectDoesNotExist:
      return error_response("Team not found")
    team.delete()
    return Response({})

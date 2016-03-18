from django.contrib.auth import authenticate, login, logout
from django.contrib.auth import get_user_model
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

    team_data = request.data
    if not ('username' in team_data and 'teamname' in team_data and 'email' in team_data and 'password' in team_data):
      return registration_response(False, error='Invalid parameters')

    username = team_data['username']
    teamname = team_data['teamname']
    email = team_data['email']
    password = team_data['password']

    # validate email
    try:
      EmailValidator(email)
    except ValidationError as e:
      return registration_response(False, error=e.message, errorfields={'email': True})

    # check if email exists for ctf or global
    User = get_user_model()
    enc_email = User.objects.encrypt_email(email, ctf)
    check = User.objects.filter(enc_email__iexact=enc_email) or User.objects.filter(enc_email__iexact=email)
    if check:
      return registration_response(False, error='Email is taken', errorfields={'email': True})

    # check if teamname exists for ctf or global
    enc_teamname = Team.objects.encrypt_teamname(teamname, ctf)
    check = Team.objects.filter(enc_teamname__iexact=enc_teamname) or Team.objects.filter(enc_teamname__iexact=teamname)
    if check:
      return registration_response(False, error='Team name is taken', errorfields={'teamname': True})
    if len(teamname) > 30:
      return registration_response(False, error='Teamname too long, 30 characters max')

    # check if username exists for ctf or global
    enc_username = User.objects.encrypt_username(username, ctf)
    check = User.objects.filter(enc_username__iexact=enc_username) or User.objects.filter(enc_username__iexact=username)
    if check:
      return registration_response(False, error='Username is taken', errorfields={'username': True})
    if len(username) > 30:
      return registration_response(False, error='Username too long, 30 characters max')

    # Create temp user to validate input
    temp_user = User(
      enc_username=enc_username,
      username=username,
      ctf=ctf,
      enc_email=enc_email,
      email=email,
      password=password
    )
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
    new_user = User.objects.create_user(username, ctf, email, password)
    new_team = Team.objects.create_team(teamname, new_user, ctf)

    # Registration was successful! Now login the new user.
    user = authenticate(enc_username=enc_username, password=password)
    if user is not None and user.is_active:
      login(request, user)
      return registration_response(True, user)
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
      return error_response(error='Team not found')

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
    try:
      if str(request.user.team.id) != id and not request.user.is_staff:
        return error_response(error='You do not have permission to edit this team')
    except ObjectDoesNotExist:
      if not request.user.is_staff:
        return error_response(error='You do not have permission to edit this team')

    if 'team' not in request.data:
      return error_response(error='Team not given',)
    team_data = request.data['team']

    try:
      team = Team.objects.get(id=id)
    except ObjectDoesNotExist:
      return error_response(error='Team not found')

    user = team.user
    if team.scoreboard:
      ctf = scoreboard.ctf
    else:
      ctf = None

    if 'email' not in team_data:
      return error_response(error='Email not given', errorfields={'email': True})
    email = team_data['email']

    if 'password' in team_data:
      password = team_data['password']
    else:
      password = None

    # validate email
    try:
      EmailValidator(email)
    except ValidationError as e:
      return error_response(error=e.message, errorfields={'email': True})

    # check if email exists for ctf or global
    User = get_user_model()
    if ctf:
      enc_email = User.objects.encrypt_email(email, ctf)
      check = User.objects.exclude(id=user.id).filter(enc_email__iexact=enc_email) or User.objects.exclude(id=user.id).filter(enc_email__iexact=email)
    else:
      check = User.objects.exclude(id=user.id).filter(enc_email__iexact=email)
    if check:
      return error_response(error='Email taken', errorfields={'email': True})

    # add enc_teamname/teamname checks here
    # add enc_username/username checks here

    # if non-admin do email-authentication tokens here
    if ctf:
      user.enc_email = User.objects.encrypt_email(email, ctf)
      user.email = email
    else:
      user.enc_email = email
      user.email = email
    #team.is_hidden = hidden
    if password:
      user.set_password(password)

    try:
      user.save()
      team.save()
    except IntegrityError:
      return error_response(error='Error modifying team')

    # django logs user out on password change, so re-login
    if password and request.user.id == user.id:
      if ctf:
        enc_username = User.objects.encrypt_username(request.user.username, ctf)
        _user = authenticate(enc_username=enc_username, password=password)
      else:
        _user = authenticate(enc_username=request.user.username, password=password)
      if _user is not None and _user.is_active:
        login(request, _user)

    # change this to be similar to session if modifying request.user
    if request.user.is_staff:
      serialized_team = AdminTeamSerializer(team, many=False, context={'request': request})
    else:
      serialized_team = TeamSerializer(team, many=False, context={'request': request})
    return Response({
      'team': serialized_team.data,
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

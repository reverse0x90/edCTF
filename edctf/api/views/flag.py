from django.core.exceptions import ObjectDoesNotExist
from ratelimit.decorators import ratelimit
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from edctf.api.models import Challenge, ChallengeTimestamp
from edctf.api.permissions import FlagPermission, FlagPermissionDetail


def update_solved(team, challenge):
  """
  Updates the database points for a given team.
  """
  # Save the time that the challenge was solved.
  timestamp = ChallengeTimestamp.objects.create(team=team, challenge=challenge)
  timestamp.save()

  # Update the team points and last timestamp in the database.
  team.last_timestamp = timestamp.created
  team.save()
  challenge.save()

def check_flag(team, challenge, flag):
  """
  Checks a given flag against the challenge flag.
  """
  # Check if team has already solved the challenge.
  res = team.solved.filter(id=challenge.id)
  error = None

  # If the team has not solved the challenge, check the flag else the team
  # has already solved the challenge so return an error message.
  if not res:
    # TODO: Allow for regex flag checking in the future
    correct = challenge.flag == flag
    # If the user input the correct flag, update the team's correct flag
    # count else update the wrong flags count and return an error.
    if correct:
      team.correctflags = team.correctflags + 1
      team.save()

      # update timestamps
      update_solved(team, challenge)
      return True, error
    else:
      error = 'Invalid flag'
      team.wrongflags = team.wrongflags + 1
      team.save()
      return False, error
  else:
    error = 'Already solved'
    return False, error


class FlagView(APIView):
  """
  Manages flag statistic data requests.
  """
  permission_classes = (FlagPermission,)

  def error_response(self, error, errorfields={}):
    """
    Handles error messages
    """
    return Response({
      'errors': {
        'message': error,
        'fields': errorfields,
      },
    }, status=status.HTTP_400_BAD_REQUEST)


class FlagViewDetail(APIView):
  """
  Manages flag submit and statistics by challenge id requests.
  """
  permission_classes = (FlagPermissionDetail,)

  def success_response(self, message):
    """
    Handles successful message responses
    """
    return Response({
      'success': {
        'message': message,
      },
    })

  def error_response(self, error, errorfields={}):
    """
    Handles error messages
    """
    return Response({
      'errors': {
        'message': error,
        'fields': errorfields,
      },
    }, status=status.HTTP_400_BAD_REQUEST)

  @ratelimit(key='ip', rate='10/m')
  @ratelimit(key='user', rate='30/m')
  def post(self, request, challenge_id, format=None):
    """
    Handles flag submit for challenge id
    """
    was_limited = getattr(request, 'limited', False)
    if was_limited:
      return self.error_response('Too many flags submitted')

    try:
      challenge = Challenge.objects.get(id=challenge_id)
    except ObjectDoesNotExist:
      return self.error_response('Challenge not found')

    if 'flag' not in request.data or not request.data['flag']:
      return self.error_response('Flag not given')

    flag_data = request.data['flag']
    if 'key' not in flag_data or not flag_data['key']:
      return self.error_response('Flag key not given')

    key = flag_data['key']

    try:
      if not request.user.team:
        return self.error_response('No team associated with user')
    except ObjectDoesNotExist:
      return self.error_response('No team associated with user')

    team = request.user.team
    success, error = check_flag(team, challenge, key)
    if success:
      return self.success_response('Correct flag')
    else:
      return self.error_response(error)

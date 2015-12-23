from ratelimit.decorators import ratelimit
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from edctf.api.models import Challenge, ChallengeTimestamp
from edctf.api.permissions import ChallengePermission
from edctf.api.serializers import ChallengeSerializer


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
      return True, error
    else:
      error = 'Invalid flag'
      team.wrongflags = team.wrongflags + 1
      team.save()
      return False, error
  else:
    error = 'Already solved'
    return False, error


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


class ChallengeView(APIView):
  """
  Manages challenge requests.
  """
  permission_classes = (ChallengePermission,)

  def form_response(self, success, error=''):
    """
    Returns the challenge form response.
    """
    # Create return data dictionary
    data = {
      'success': success,
    }
    # If error during flag check, return the error else return
    # the flag response data.
    if error:
      data['error'] = error
    return Response(data)

  def get(self, request, id=None, format=None):
    """
    Gets all challenges or gets an individual challenge via
    challenge/:id.
    """
    # If a specific challenge is requested, return that challege
    # else return all the challenges in the database.
    if id:
      challenges = Challenge.objects.filter(id=id)
    else:
      challenges = Challenge.objects.all()

    # Serialize challenge object and return the serialized data.
    serialized_challenges = ChallengeSerializer(challenges, many=True, context={'request': request})
    return Response({
      'challenges': serialized_challenges.data,
    })

  @ratelimit(key='ip', rate='10/m')
  @ratelimit(key='user', rate='30/m')
  def post(self, request, id=None, format=None):
    """
    Checks a submitted flag for a challenge.
    """
    # Verify the challege exists
    if id:
      was_limited = getattr(request, 'limited', False)
      if was_limited:
        return self.form_response(False, 'Too many flags submitted')
      
      try:
        _challenge = Challenge.objects.get(id=id)
      except:
        return Response(status=status.HTTP_404_NOT_FOUND)

      # Get the flag data from the request json object.
      flag_data = request.data

      # Verify flag is not blank and was set in the request.
      if 'flag' not in flag_data:
        return Response(status=status.HTTP_400_BAD_REQUEST)

      flag = flag_data['flag']

      # Get the team object associated with the user's session.
      _team = request.user.teams

      # Check if the flag is correct and return the result.
      success, error = check_flag(_team, _challenge, flag)
      if success:
        update_solved(_team, _challenge)
        return self.form_response(True)
      else:
        return self.form_response(False, error)
    else:
      return Response(status=status.HTTP_404_NOT_FOUND)

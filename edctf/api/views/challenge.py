from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from edctf.api.models import challenge, challengeTimestamp
from edctf.api.serializers import challengeSerializer
import json


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
            team.correct_flags = team.correct_flags + 1
            team.save()
            return True, error
        else:
            error = 'Invalid flag'
            team.wrong_flags = team.wrong_flags + 1
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
    timestamp = challengeTimestamp.objects.create(team=team, challenge=challenge)
    timestamp.save()

    # Update the team points and last timestamp in the database.
    team.points = team.points + challenge.points
    team.last_timestamp = timestamp.created
    team.save()
    challenge.save()


class challengeView(APIView):
    """
    Manages challenge requests.
    """
    permission_classes = (IsAuthenticated,)

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
            challenges = challenge.objects.filter(id=id)
        else:
            challenges = challenge.objects.all()
        
        # Serialize challenge object and return the serialized data.
        challenge_serializer = challengeSerializer(challenges, many=True, context={'request': request})
        return Response({
            "challenges": challenge_serializer.data,
        })


    def post(self, request, id=None, format=None):
        """
        Checks a submitted flag for a challenge.
        """
        # Verify the challege exists
        if id:
            try:
                _challenge = challenge.objects.get(id=id)
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
            success, error = check_flag(_team,_challenge, flag)
            if success:
                update_solved(_team, _challenge)
                return self.form_response(True)
            else:
                return self.form_response(False, error)
        else:
            return Response(status=status.HTTP_404_NOT_FOUND)

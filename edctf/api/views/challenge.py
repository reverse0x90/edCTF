from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from edctf.api.models import challenge, challengeTimestamp
from edctf.api.serializers import challengeSerializer
import json


def check_flag(team, challenge, flag):
    '''
    Checks a given flag with a challenge.
    '''
    res = team.solved.filter(id=challenge.id)
    error = None

    # if not solved, do flag check
    if not res:
        # Allow regex in the future
        correct = challenge.flag == flag
        if correct:
            team.correct_flags = team.correct_flags + 1
            team.save()
            return True, error
        else:
            error = 'Invalid flag'
            team.wrong_flags = team.wrong_flags + 1
            team.save()
            return False, error
    # already solved
    else:
        error = 'Already solved'
        team.wrong_flags = team.wrong_flags + 1
        team.save()
        return False, error

def update_solved(team, challenge):
    '''
    Gives points to a given user
    '''
    #team.solved.add(challenge)
    timestamp = challengeTimestamp.objects.create(team=team, challenge=challenge)
    timestamp.save()

    team.points = team.points + challenge.points
    team.last_timestamp = timestamp.created
    team.save()
    challenge.save()

class challengeView(APIView):
    permission_classes = (IsAuthenticated,)

    
    def form_response(self, success, error=''):
        data = {
            'success': success,
        }
        if error:
            data['error'] = error
        return Response(data)

    def get(self, request, id=None, format=None):
        """
        Get all challenge
        or get by id via challenge/:id
        """
        if id:
            challenges = challenge.objects.filter(id=id)
        else:
            challenges = challenge.objects.all()
        challenge_serializer = challengeSerializer(challenges, many=True, context={'request': request})
        return Response({
            "challenges": challenge_serializer.data,
        })
    def post(self, request, id=None, format=None):
        """
        Submit a flag for a challenge
        """
        if id:
            try:
                _challenge = challenge.objects.get(id=id)
            except:
                return Response(status=status.HTTP_404_NOT_FOUND)
            
            flag_data = json.loads(request.body)
            if 'flag' not in flag_data:
                return Response(status=status.HTTP_400_BAD_REQUEST)
            flag = flag_data['flag']

            _team = request.user.teams
            success, error = check_flag(_team,_challenge, flag)
            if success:
                update_solved(_team, _challenge)
                return self.form_response(True)
            else:
                return self.form_response(False, error)
        else:
            return Response(status=status.HTTP_404_NOT_FOUND)

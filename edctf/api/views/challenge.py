from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from edctf.api.models import challenge, challengeTimestamp
from edctf.api.serializers import challengeSerializer


def check_flag(team, challenge, flag):
    '''
    Checks a given flag with a challenge.
    '''
    res = team.solved.filter(id=challenge.id)
    
    # if not solved, do flag check
    if not res:
        # Allow regex in the future
        correct1 = challenge.flag == flag
        correct2 = challenge.flag == str('null{'+flag+'}')
        correct = correct1 or correct2
        if correct:
            team.correct_flags = team.correct_flags + 1
            team.save()
            return True
        else:
            team.wrong_flags = team.wrong_flags + 1
            team.save()
            return False
    # already solved
    else:
        team.wrong_flags = team.wrong_flags + 1
        team.save()
        return False

def check_flag2(challenge, flag):
    '''
    Checks a given flag with a challenge, doesnt update db, doesnt need team
    '''

    # Allow regex in the future
    correct1 = challenge.flag == flag
    correct2 = challenge.flag == str('null{'+flag+'}')
    correct = correct1 or correct2
    if correct:
        return True
    else:
        return False

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
        '''
        Submit a flag for a challenge
        '''
        if id:
            try:
                _challenge = challenge.objects.get(id=id)
            except:
                return Response({
                    "success": False
                }, status=status.HTTP_404_NOT_FOUND)
            
            flag = request.POST.get('flag')
            if not flag:
                return Response({
                    "success": False
                }, status=status.HTTP_401_UNAUTHORIZED)

            _team = request.user.teams
            if check_flag(_team,_challenge, flag):
                update_solved(_team, _challenge)
                return Response({
                    "success": True
                })
            else:
                return Response({
                    "success": False
                })
        else:
            return Response(status=status.HTTP_401_UNAUTHORIZED)

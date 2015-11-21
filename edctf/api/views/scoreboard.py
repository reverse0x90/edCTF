from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from edctf.api.models import scoreboard, team
from edctf.api.serializers import scoreboardSerializer, teamSerializer
import time


def get_topteamsdata(teams):
    data = {}
    data['xs'] = {}
    data['type'] = 'step'
    data['columns'] = []

    current_time = int(time.time())
    #start = current_time - (60*60*12) # only show past 12 hours
    delta_initial_point_timestamp = 60*5

    points = initial_points = 0
    for position,team in enumerate(teams):
        time_data = [str(position)]
        point_data = [team.teamname]
        
        challengeTimestamps = team.challengeTimestamps.order_by('created')
        for i,challengeTimestamp in enumerate(challengeTimestamps):
            timestamp = int(time.mktime(challengeTimestamp.created.timetuple()))
            if i == 0:
                time_data.append(timestamp-delta_initial_point_timestamp)
                point_data.append(points)
            points = points + challengeTimestamp.challenge.points
            #if timestamp < start:
            #    continue
            

            time_data.append(timestamp)
            point_data.append(points)
        time_data.append(current_time)
        point_data.append(team.points)
        data['xs'][team.teamname] = str(position)
        data['columns'].append(time_data)
        data['columns'].append(point_data)
        points = initial_points
    return data

class scoreboardView(APIView):
    permission_classes = (AllowAny,)
    def get(self, request, id=None, format=None):
        """
        Get all scoreboards
        or get by id via scoreboards/:id
        """
        if id:
            # Set scoreboard object
            scoreboards = scoreboard.objects.filter(id=id)
            scoreboards_serializer = scoreboardSerializer(scoreboards, many=True, context={'request': request})
            
            # Set teams from scoreboard
            teams = team.objects.filter(scoreboard=scoreboards[0]).order_by('-points','-last_timestamp')
            teams_serializer = teamSerializer(teams, many=True, context={'request': request})
            for pos,t in enumerate(teams_serializer.data):
                t['position'] = pos+1

            # Create top teams c3 data
            scoreboards_serializer.data[0]['topteamsdata'] = get_topteamsdata(teams[:scoreboards[0].numtopteams])

            return Response({
                "scoreboards": scoreboards_serializer.data,
                "teams": teams_serializer.data,
            })

        else:
            scoreboards = scoreboard.objects.all()
            scoreboards_serializer = scoreboardSerializer(scoreboards, many=True, context={'request': request})
            return Response({
                "scoreboards": scoreboards_serializer.data,
            })

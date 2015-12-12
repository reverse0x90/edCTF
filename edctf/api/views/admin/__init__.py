from rest_framework.permissions import IsAdminUser
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from edctf.api.models import ctf, challengeboard, category, challenge, scoreboard, team
from edctf.api.serializers import admin


class CtfViewSet(ModelViewSet):
    permission_classes = (IsAdminUser,)
    queryset = ctf.objects.all()
    serializer_class = admin.CtfSerializer

class ChallengeboardViewSet(ModelViewSet):
    permission_classes = (IsAdminUser,)
    queryset = challengeboard.objects.all()
    serializer_class = admin.ChallengeboardSerializer

class CategoryViewSet(ModelViewSet):
    permission_classes = (IsAdminUser,)
    queryset = category.objects.all()
    serializer_class = admin.CategorySerializer

class ChallengeViewSet(ModelViewSet):
    permission_classes = (IsAdminUser,)
    queryset = challenge.objects.all()
    serializer_class = admin.ChallengeSerializer

class ScoreboardViewSet(ModelViewSet):
    permission_classes = (IsAdminUser,)
    queryset = scoreboard.objects.all()
    serializer_class = admin.ScoreboardSerializer

class TeamViewSet(ModelViewSet):
    permission_classes = (IsAdminUser,)
    queryset = team.objects.all()
    serializer_class = admin.TeamSerializer

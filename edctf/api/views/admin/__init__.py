from rest_framework.permissions import IsAdminUser
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from edctf.api.models import Ctf, Challengeboard, Category, Challenge, Scoreboard, Team
from edctf.api.serializers import admin


class CtfViewSet(ModelViewSet):
    permission_classes = (IsAdminUser,)
    queryset = Ctf.objects.all()
    serializer_class = admin.CtfSerializer


class ChallengeboardViewSet(ModelViewSet):
    permission_classes = (IsAdminUser,)
    queryset = Challengeboard.objects.all()
    serializer_class = admin.ChallengeboardSerializer


class CategoryViewSet(ModelViewSet):
    permission_classes = (IsAdminUser,)
    queryset = Category.objects.all()
    serializer_class = admin.CategorySerializer


class ChallengeViewSet(ModelViewSet):
    permission_classes = (IsAdminUser,)
    queryset = Challenge.objects.all()
    serializer_class = admin.ChallengeSerializer


class ScoreboardViewSet(ModelViewSet):
    permission_classes = (IsAdminUser,)
    queryset = Scoreboard.objects.all()
    serializer_class = admin.ScoreboardSerializer


class TeamViewSet(ModelViewSet):
    permission_classes = (IsAdminUser,)
    queryset = Team.objects.all()
    serializer_class = admin.TeamSerializer

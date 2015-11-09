from rest_framework import serializers

#load django and webapp models
from django.contrib.auth.models import *
from edctf.api.models import *


class ctfSerializer(serializers.ModelSerializer):
    class Meta:
        model = ctf
        fields = ('id', 'name', 'live', 'challengeboard', 'scoreboard')

class challengeboardSerializer(serializers.ModelSerializer):
    class Meta:
        model = challengeboard
        fields = ('id', 'categories')

class categorySerializer(serializers.ModelSerializer):
    class Meta:
        model = category
        fields = ('id', 'name', 'challenges')

class challengeSerializer(serializers.ModelSerializer):
    class Meta:
        model = challenge
        fields = ('id', 'title', 'points', 'description', 'solved', 'num_solved')

class scoreboardSerializer(serializers.ModelSerializer):
    class Meta:
        model = scoreboard
        fields = ('id', 'numtopteams', 'teams')

class teamSerializer(serializers.ModelSerializer):
    class Meta:
        model = team
        fields = ('id', 'teamname', 'points', 'correct_flags', 'wrong_flags', 'solved')

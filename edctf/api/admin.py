from django.contrib import admin
from edctf.api.models import *


# Register your models here.
class CtfAdmin(admin.ModelAdmin):
  """
  Sets the display for the ctf model in the django admin interface.
  """
  list_display = ('name', 'online')


class ChallengeboardAdmin(admin.ModelAdmin):
  """
  Sets the display for the challengeboard model in the django admin
  interface.
  """
  list_display = ('id',)


class CategoryAdmin(admin.ModelAdmin):
  """
  Sets the display settings for the category model in the django admin
  interface.
  """
  list_display = ('name',)


class ChallengeAdmin(admin.ModelAdmin):
  """
  Sets the display settings for the challenge model in the django admin
  interface.
  """
  list_display = ('category', 'points', 'title')


class ScoreboardAdmin(admin.ModelAdmin):
  """
  Sets the display settings for the scoreboard model in the django admin
  interface.
  """
  list_display = ('id',)


class TeamAdmin(admin.ModelAdmin):
  """
  Sets the display settings for the team model in the django admin
  interface.
  """
  list_display = ('teamname', 'points', 'ctfname')


class ChallengeTimestampAdmin(admin.ModelAdmin):
  """
  Sets the display settings for the challenge_timestamp model in the django
  admin interface.
  """
  list_display = ('team', 'challenge', 'created')


# Register the models to the django admin interface.
admin.site.register(Ctf, CtfAdmin)
admin.site.register(Challengeboard, ChallengeboardAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Challenge, ChallengeAdmin)
admin.site.register(Scoreboard, ScoreboardAdmin)
admin.site.register(Team, TeamAdmin)
admin.site.register(ChallengeTimestamp, ChallengeTimestampAdmin)

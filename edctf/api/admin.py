from django.contrib import admin
from edctf.api.models import *


# Register your models here.
class ctf_admin(admin.ModelAdmin):
  """
  Sets the display for the ctf model in the django admin interface.
  """
  list_display = ('name', 'live')


class challengeboard_admin(admin.ModelAdmin):
  """
  Sets the display for the challengeboard model in the django admin
  interface.
  """
  list_display = ('id',)

  def ctf_name(self, obj):
    return obj.ctf


class category_admin(admin.ModelAdmin):
  """
  Sets the display settings for the category model in the django admin
  interface.
  """
  list_display = ('name',)


class challenge_admin(admin.ModelAdmin):
  """
  Sets the display settings for the challenge model in the django admin
  interface.
  """
  list_display = ('category', 'points', 'title')


class scoreboard_admin(admin.ModelAdmin):
  """
  Sets the display settings for the scoreboard model in the django admin
  interface.
  """
  list_display = ('id',)

  def ctf_name(self, obj):
    return obj.ctf


class team_admin(admin.ModelAdmin):
  """
  Sets the display settings for the team model in the django admin
  interface.
  """
  list_display = ('teamname', 'points')


class challenge_timestamp_admin(admin.ModelAdmin):
  """
  Sets the display settings for the challenge_timestamp model in the django
  admin interface.
  """
  list_display = ('team', 'challenge', 'created')

# Register the models to the django admin interface.
admin.site.register(ctf, ctf_admin)
admin.site.register(challengeboard, challengeboard_admin)
admin.site.register(category, category_admin)
admin.site.register(challenge, challenge_admin)
admin.site.register(scoreboard, scoreboard_admin)
admin.site.register(team, team_admin)
admin.site.register(challenge_timestamp, challenge_timestamp_admin)

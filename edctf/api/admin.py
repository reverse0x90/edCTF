from django.contrib import admin
from edctf.api.models import *


# Register your models here.
class ctfAdmin(admin.ModelAdmin):
  """
  Sets the display for the ctf model in the django admin interface.
  """
  list_display = ('name', 'live')


class challengeboardAdmin(admin.ModelAdmin):
  """
  Sets the display for the challengeboard model in the django admin
  interface.
  """
  list_display = ('id',)

  def ctf_name(self, obj):
    return obj.ctf


class categoryAdmin(admin.ModelAdmin):
  """
  Sets the display settings for the category model in the django admin
  interface.
  """
  list_display = ('name',)


class challengeAdmin(admin.ModelAdmin):
  """
  Sets the display settings for the challenge model in the django admin
  interface.
  """
  list_display = ('category', 'points', 'title')


class scoreboardAdmin(admin.ModelAdmin):
  """
  Sets the display settings for the scoreboard model in the django admin
  interface.
  """
  list_display = ('id',)

  def ctf_name(self, obj):
    return obj.ctf


class teamAdmin(admin.ModelAdmin):
  """
  Sets the display settings for the team model in the django admin
  interface.
  """
  list_display = ('teamname', 'points')


class challengeTimestampAdmin(admin.ModelAdmin):
  """
  Sets the display settings for the challengeTimestamp model in the django
  admin interface.
  """
  list_display = ('team', 'challenge', 'created')

# Register the models to the django admin interface.
admin.site.register(ctf, ctfAdmin)
admin.site.register(challengeboard, challengeboardAdmin)
admin.site.register(category, categoryAdmin)
admin.site.register(challenge, challengeAdmin)
admin.site.register(scoreboard, scoreboardAdmin)
admin.site.register(team, teamAdmin)
admin.site.register(challengeTimestamp, challengeTimestampAdmin)

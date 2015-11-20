from django.contrib import admin
from edctf.api.models import *

# Register your models here.
class ctfAdmin(admin.ModelAdmin):
    list_display = ('name', 'live')

class challengeboardAdmin(admin.ModelAdmin):
    list_display = ('id',)
    def ctf_name(self, obj):
        return obj.ctf

class categoryAdmin(admin.ModelAdmin):
    list_display = ('name',)

class challengeAdmin(admin.ModelAdmin):
    list_display = ('category', 'points', 'title')

class scoreboardAdmin(admin.ModelAdmin):
    list_display = ('id',)
    def ctf_name(self, obj):
        return obj.ctf

class teamAdmin(admin.ModelAdmin):
    list_display = ('teamname','points')

class challengeTimestampAdmin(admin.ModelAdmin):
    list_display = ('team','challenge','created')


admin.site.register(ctf, ctfAdmin)
admin.site.register(challengeboard, challengeboardAdmin)
admin.site.register(category, categoryAdmin)
admin.site.register(challenge, challengeAdmin)
admin.site.register(scoreboard, scoreboardAdmin)
admin.site.register(team, teamAdmin)
admin.site.register(challengeTimestamp, challengeTimestampAdmin)


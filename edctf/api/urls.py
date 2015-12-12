from django.conf.urls import include, url
from rest_framework import routers
from edctf.api import views
from edctf.api.views import admin


router = routers.SimpleRouter(trailing_slash=False)
router.register(r'ctfs', admin.CtfViewSet)
router.register(r'challenges', admin.ChallengeboardViewSet)
router.register(r'categories', admin.CategoryViewSet)
router.register(r'challenges', admin.ChallengeViewSet)
router.register(r'scoreboards', admin.ScoreboardViewSet)
router.register(r'TeamViewSet', admin.TeamViewSet)

urlpatterns = [
  url(r'^session/?$', views.session_view.as_view()),
  url(r'^ctfs/?$', views.ctf_view.as_view()),
  url(r'^ctfs/(?P<id>\d+)/?$', views.ctf_view.as_view()),
  url(r'^challengeboards/?$', views.challengeboard_view.as_view()),
  url(r'^challengeboards/(?P<id>\d+)/?$', views.challengeboard_view.as_view()),
  url(r'^challenges/?$', views.challenge_view.as_view()),
  url(r'^challenges/(?P<id>\d+)/?$', views.challenge_view.as_view()),
  url(r'^scoreboards/?$', views.scoreboard_view.as_view()),
  url(r'^scoreboards/(?P<id>\d+)/?$', views.scoreboard_view.as_view()),
  url(r'^teams/?$', views.team_view.as_view()),
  url(r'^teams/(?P<id>\d+)/?$', views.team_view.as_view()),
  url(r'^ctftime/(?P<id>\d+)/?$', views.ctftime_view.as_view()),
  url(r'^admin/', include(router.urls)),
]

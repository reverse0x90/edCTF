from django.conf.urls import include, url
from rest_framework import routers
from edctf.api import views
from rest_framework.urlpatterns import format_suffix_patterns


router = routers.DefaultRouter()

urlpatterns = [
  url(r'^', include(router.urls)),
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
]

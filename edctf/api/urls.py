from django.conf.urls import include, url
from rest_framework import routers
from edctf.api import views


urlpatterns = []

# general routes
urlpatterns += [
  url(r'^categories/?$', views.CategoryView.as_view()),
  url(r'^challengeboards/?$', views.ChallengeboardView.as_view()),
  url(r'^challenges/?$', views.ChallengeView.as_view()),
  url(r'^ctfs/?$', views.CtfView.as_view()),
  url(r'^flags/?$', views.FlagView.as_view()),
  url(r'^scoreboards/?$', views.ScoreboardView.as_view()),
  url(r'^session/?$', views.SessionView.as_view()),
  url(r'^teams/?$', views.TeamView.as_view()),
]

# routes by id
urlpatterns += [
  url(r'^abouts/(?P<id>\d+)/?$', views.CtfAboutViewDetail.as_view()),
  url(r'^categories/(?P<id>\d+)/?$', views.CategoryViewDetail.as_view()),
  url(r'^challenges/(?P<id>\d+)/?$', views.ChallengeViewDetail.as_view()),
  url(r'^challengeboards/(?P<id>\d+)/?$', views.ChallengeboardViewDetail.as_view()),
  url(r'^ctfs/(?P<id>\d+)/?$', views.CtfViewDetail.as_view()),
  url(r'^ctftime/(?P<ctf_id>\d+)/?$', views.CtftimeViewDetail.as_view()),
  url(r'^flags/(?P<challenge_id>\d+)/?$', views.FlagViewDetail.as_view()),
  url(r'^homes/(?P<id>\d+)/?$', views.CtfHomeViewDetail.as_view()),
  url(r'^scoreboards/(?P<id>\d+)/?$', views.ScoreboardViewDetail.as_view()),
  url(r'^teams/(?P<id>\d+)/?$', views.TeamViewDetail.as_view()),
]

from django.conf.urls import include, url
from rest_framework import routers
from edctf.api import views


#router = routers.SimpleRouter(trailing_slash=False)

urlpatterns = []

# general routes
urlpatterns += [
  url(r'^session/?$', views.SessionView.as_view()),
  url(r'^ctfs/?$', views.CtfView.as_view()),
  url(r'^challengeboards/?$', views.ChallengeboardView.as_view()),
  url(r'^categories/?$', views.CategoryView.as_view()),
  url(r'^challenges/?$', views.ChallengeView.as_view()),
  url(r'^scoreboards/?$', views.ScoreboardView.as_view()),
  url(r'^teams/?$', views.TeamView.as_view()),
]

# routes by id
urlpatterns += [
  url(r'^ctfs/(?P<id>\d+)/?$', views.CtfViewDetail.as_view()),
  url(r'^challengeboards/(?P<id>\d+)/?$', views.ChallengeboardView.as_view()),
  url(r'^categories/(?P<id>\d+)/?$', views.CategoryViewDetail.as_view()),
  url(r'^challenges/(?P<id>\d+)/?$', views.ChallengeView.as_view()),
  url(r'^scoreboards/(?P<id>\d+)/?$', views.ScoreboardView.as_view()),
  url(r'^teams/(?P<id>\d+)/?$', views.TeamView.as_view()),
  url(r'^ctftime/(?P<id>\d+)/?$', views.CtftimeView.as_view()),
]

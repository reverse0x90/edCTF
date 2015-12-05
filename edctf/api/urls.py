from django.conf.urls import include, url
from rest_framework import routers
from edctf.api import views
from rest_framework.urlpatterns import format_suffix_patterns


router = routers.DefaultRouter()

urlpatterns = [
  url(r'^', include(router.urls)),
  url(r'^session/?$', views.sessionView.as_view()),
  url(r'^ctfs/?$', views.ctfView.as_view()),
  url(r'^ctfs/(?P<id>\d+)/?$', views.ctfView.as_view()),
  url(r'^challengeboards/?$', views.challengeboardView.as_view()),
  url(r'^challengeboards/(?P<id>\d+)/?$', views.challengeboardView.as_view()),
  url(r'^challenges/?$', views.challengeView.as_view()),
  url(r'^challenges/(?P<id>\d+)/?$', views.challengeView.as_view()),
  url(r'^scoreboards/?$', views.scoreboardView.as_view()),
  url(r'^scoreboards/(?P<id>\d+)/?$', views.scoreboardView.as_view()),
  url(r'^teams/?$', views.teamView.as_view()),
  url(r'^teams/(?P<id>\d+)/?$', views.teamView.as_view()),
]

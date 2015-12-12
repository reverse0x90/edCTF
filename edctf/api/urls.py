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
  url(r'^session/?$', views.SessionView.as_view()),
  url(r'^ctfs/?$', views.CtfView.as_view()),
  url(r'^ctfs/(?P<id>\d+)/?$', views.CtfView.as_view()),
  url(r'^challengeboards/?$', views.ChallengeboardView.as_view()),
  url(r'^challengeboards/(?P<id>\d+)/?$', views.ChallengeboardView.as_view()),
  url(r'^challenges/?$', views.ChallengeView.as_view()),
  url(r'^challenges/(?P<id>\d+)/?$', views.ChallengeView.as_view()),
  url(r'^scoreboards/?$', views.ScoreboardView.as_view()),
  url(r'^scoreboards/(?P<id>\d+)/?$', views.ScoreboardView.as_view()),
  url(r'^teams/?$', views.TeamView.as_view()),
  url(r'^teams/(?P<id>\d+)/?$', views.TeamView.as_view()),
  url(r'^ctftime/(?P<id>\d+)/?$', views.CtftimeView.as_view()),
  url(r'^admin/', include(router.urls)),
]

from django.conf.urls import include, url

#Django Rest Framework
from rest_framework import routers
from edctf.api import views
from rest_framework.urlpatterns import format_suffix_patterns

#REST API routes
router = routers.DefaultRouter()

#REST API
urlpatterns = [
    url(r'^', include(router.urls)),
    url(r'^ctfs/?$', views.ctf),
    url(r'^ctfs/(?P<id>\d+)/?$', views.ctf),
    url(r'^challengeboards/?$', views.challengeboard),
    url(r'^challengeboards/(?P<id>\d+)/?$', views.challengeboard),
    url(r'^scoreboards/?$', views.scoreboard),
    url(r'^scoreboards/(?P<id>\d+)/?$', views.scoreboard),
]
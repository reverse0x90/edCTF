from django.conf.urls import include, url
from django.contrib import admin
from django.conf import settings
from edctf.api import views


urlpatterns = [
  url(r'^api/', include('edctf.api.urls')),
  url(r'^robots\.txt$', views.robots),
  url(r'^crossdomain\.xml$', views.crossdomain),
  url(r'^djangoadmin/', include(admin.site.urls)),
  url(r'^.*$', views.home),
]

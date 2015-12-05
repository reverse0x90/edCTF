from django.conf.urls import include, url
from django.contrib import admin
from django.conf import settings
from edctf.api import views


urlpatterns = [
  url(r'^[^\/]*$', views.home),
  url(r'^robots\.txt$', views.robots),
  url(r'^crossdomain\.xml$', views.crossdomain),
  url(r'^admin/', include(admin.site.urls)),
  url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
  url(r'^api/', include('edctf.api.urls')),
]

from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include, re_path
from django.views.generic.base import TemplateView

from django.views.static import serve

urlpatterns = [
    path('a4w1n/', admin.site.urls), 
    path('', include("projectManagerDjango.urls")), 
    re_path(r'^media/(?P<path>.*)$', serve,{'document_root':       settings.MEDIA_ROOT}), 
    re_path(r'^static/(?P<path>.*)$', serve,{'document_root': settings.STATIC_ROOT}), 
	]
urlpatterns+=static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
"""sift URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
# from django.conf.urls.static import static
# from django.conf import settings

from django.views import static
from django.conf import settings
from django.conf.urls import url

from django.contrib import admin
from django.urls import path
import user.views as user
import foodlog.views as foodlog

urlpatterns = [
    path('admin/', admin.site.urls),
    path('login/', user.login),
    path('register/', user.register),
    path('logout/',user.logout),
    path('index/',foodlog.index),
    path('scan/',foodlog.scan),
    path('single-report/',foodlog.single_report),
    path('yesterday/', foodlog.yesterday_report),
    path('week/',foodlog.week_report),
    path('year/',foodlog.year_report),
    path('adjust-goal/',user.adjust_goal),
    path('update-info/',user.update_info),
    path('',foodlog.index),
    url(r'^media/(?P<path>.*)$', static.serve, {'document_root': settings.MEDIA_ROOT}, name='media'),
    # url(r'^static/(?P<path>.*)$', static.serve, {'document_root': settings.STATIC_ROOT}, name='media')
] # + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

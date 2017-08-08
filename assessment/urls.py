"""assessment URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.10/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url,include
from django.contrib import admin
from assessproject.views import error404,index,check_code,user_register,user_login,download,getsession
# from django.views.generic.base import RedirectView
from django.conf import settings
from django.views.static import serve

urlpatterns = [
    url(r'^login/$', user_login),
    url(r'^register/$',user_register),
    url(r'^admin/', admin.site.urls),
    url(r'^$', index),
    url(r'^index/$', index),
    url(r'^index/page_id=(?P<page>\d+)/$', index),
    url(r'^assess/',include('assessproject.urls')),
    url(r'^404/$',error404),  
    url(r'^check_code/$',check_code),
    url(r'^download/(?P<projectid>\d+)/$',download),
    url(r'^static/(?P<path>.*)$', serve,{'document_root': settings.STATIC_ROOT}),
    url(r'^getsession/$',getsession,name='getsession'),
]
if not settings.DEBUG:
    urlpatterns += [url(r'^static/(?P<path>.*)$', serve,{'document_root': settings.STATIC_ROOT})]
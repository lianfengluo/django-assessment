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
from django.conf.urls import url
from django.contrib import admin
from assessproject.views import *



app_name='assess'

urlpatterns = [
    # url(r'^login/$', user_login),
    url(r'^logout/$', user_logout,name='logout'),
    # url(r'^register/$',user_register),
    url(r'^profile/$',profile,name='profile'),
    # url(r'^update_profile/$',updateprofile),
    url(r'^deletedproject/$',delproject,name='delete'),
    url(r'^startproject/$',startproject,name='create'),
    url(r'^createselect/$',createselect,name='select'),
    url(r'^createselect/projectid=(?P<project_id>\d+)/$',createselect,name='modify'),
    url(r'^projectcontent/$',projectcontent,name='content'),
    url(r'^saveassess/$',saveassess,name='save'),
    # url(r'^checkcheck_code/$',checkcheck_code,name='checkcheck_code'),
    # url(r'^checkuser/$',checkuser,name='checkuser'),
    # url(r'^checkemail/$',checkemail,name='checkemail'),
    url(r'^displaydata/projectid=(?P<project_id>\d+)/$',displaydata,name='display'),
    # url(r'^displaydata/projectid=(?P<project_id>\d+)/page_id=(?P<page>\d+)/$',displaydata),
    url(r'^deletepage/projectid=(?P<project_id>\d+)/$',deletepage,name='deletepage'),

]

"""
URL configuration for surebet project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
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
from django.contrib import admin
from django.shortcuts import redirect
from django.urls import path, include
from django.conf.urls import handler404, handler500
from . import views

handler400 = 'surebet.views.handler400'
handler403 = 'surebet.views.handler403'
handler404 = 'surebet.views.handler404'
handler500 = 'surebet.views.handler500'

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', lambda req: redirect('statpoolshome')),
    path('home', lambda req: redirect('statpoolshome'), name="home"),
    path('login', views.LoginFormView.as_view(), name='login'),
	path('register', views.RegisterFormView.as_view(), name='register'),
	path('logout', views.userlogout, name='logout'),
        
    path("statpools/", include("statpools.urls")),
    #path("", include("surebetApp.urls")),
]

"""killergame URL Configuration

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
from django.urls import path
from django.conf.urls import url
from killer import views

urlpatterns = [
    url(r'admin/$', views.score_admin, name='admin'),
    url(r'^$', views.score, name='index'),
    url(r'change_kills/$', views.change_kills, name='change_kills'),
    url(r'change_wins/$', views.change_wins, name='change_wins'),
    url(r'add_user/$', views.add_user, name='add_user'),

]


from rest_framework.routers import DefaultRouter
from rest_framework import routers
from django.conf.urls import re_path
from django.urls import include, path
from . import views



urlpatterns = [
    path('', views.index, name='index'),
    path('test', views.test, name='test'),
    path('list_teams',views.get_team_details,name='list_teams'),
    path('get_puzzles',views.get_puzzles,name='get_puzzles'),
    path('register',views.register,name='register'),
    path('get_hint',views.get_hint,name='get_hint'),
    path('validation',views.validation,name='validation'),
    path('get_current_puzzle',views.get_current_puzzle,name='get_current_puzzle'),
    path('get_location_hint',views.get_location_hint,name='get_location_hint'),
    path('get_image_url',views.get_image_url,name='get_image_url'),
    path('getSecondHalf',views.getSecondHalf,name='getSecondHalf'),
    path('add_points_player',views.add_points_player,name='add_points_player'),


    re_path('add_points/(?P<team_username>[\w.@+-]+)/(?P<points>[\w.@+-]+)$', views.add_points),
    re_path('get_next_puzzle/(?P<puzzle_id>[\w.@+-]+)$', views.get_next_puzzle),

]
from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("matches", views.matches, name="matches"),
    path("participants", views.participants, name="participants"),
    path("team/<int:id>", views.team, name="team"),
    path("player/<int:id>", views.player, name="player"),
    path("match/<int:id>", views.match, name="match"),
    path("<str:crud>/match", views.crud_match, name="crud_match"),
    path("<str:crud>/player", views.crud_player, name="crud_player"),
    path("<str:crud>/team", views.crud_team, name="crud_team"),
    path("<str:crud>/result", views.crud_result, name="crud_result"),
]
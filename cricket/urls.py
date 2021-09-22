from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("matches", views.matches, name="matches"),
    path("participants", views.participants, name="participants"),
    path("team/<int:id>", views.team, name="team"),
    path("player/<int:id>", views.player, name="player"),
    path("match/<int:id>", views.match, name="match"),
    path("result/<int:id>", views.result, name="result"),
    path("<str:field>/add", views.add, name="add"),
]
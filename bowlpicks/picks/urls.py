from django.urls import path

from . import views
# from .views import RegisterView

urlpatterns = [
    path("", views.index, name="index"),
    path("account", views.account, name="account"),
    path("account/<int:userid>", views.account, name="accountid"),
    path("deletepart/<int:userid>", views.deleteParticipant, name="deletepart"),
    path("admin-page", views.adminPage, name="adminPage"),
    path("edit-picks/<int:userid>/<int:pickid>", views.editPicks, name="editPicks"),
    path("group-picks/<str:layout>/<int:userorgame>", views.groupPicks, name="groupPicksid"),
    path("group-picks", views.groupPicks, name="groupPicks"),
    path("group-picks/<str:layout>", views.groupPicks, name="groupPickslayout"),
    path("my-picks/<int:user>", views.myPicks, name="myPicksid"),
    path("my-picks", views.myPicks, name="myPicks"),
    path("login", views.login, name="login"),
    path("register", views.register, name="register"),
    path("setup", views.setup, name="setup"),
    path("setup/<int:gameid>", views.setup, name="setupid"),
    path("logout", views.logout_view, name="logout"),
    path("deletegame/<int:gameid>", views.deleteGame, name="delete_game"),
    path("deleteteam/<int:teamid>", views.deleteTeam, name="delete_team"),
    path("addteam", views.addTeam, name="addteam"),
    path("addteam/<int:teamid>", views.addTeam, name="addteamid"),
    path("my-participants", views.myParticipants, name="myParticipants"),
    path("my-participants/<int:participantid>", views.myParticipants, name="myParticipantsid"),
]
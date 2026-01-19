from django.urls import path
from pages.views import pages_view, register_view, login_view, logout_view, edit_note, delete_note

urlpatterns = [
    path('', pages_view, name = "home"),
    path("register/", register_view, name = "register"),
    path("login/", login_view, name = "login"),
    path("logout/", logout_view, name = "logout"),
    path("edit/<int:note_id>/", edit_note, name = "edit_note"),
    path("delete/<int:note_id>/", delete_note, name = "delete_note")
]

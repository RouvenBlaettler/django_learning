from django.urls import path
from pages.views import pages_view, register_view, login_view, logout_view

urlpatterns = [
    path('', pages_view, name = "home"),
    path("register/", register_view, name = "register"),
    path("login/", login_view, name = "login"),
    path("logout/", logout_view, name = "logout")
]

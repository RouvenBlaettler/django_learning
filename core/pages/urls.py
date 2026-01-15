from django.urls import path
from pages.views import pages_view

urlpatterns = [
    path('', pages_view, name = "home"),
]

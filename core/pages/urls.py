from django.urls import path
from pages.views import pages_view

url_patterns = [
    path('', pages_view, name = "home"),
]

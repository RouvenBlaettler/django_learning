from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.
def pages_view(request):
    return HttpResponse("Hello Django")
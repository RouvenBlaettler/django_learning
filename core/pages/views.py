from django.shortcuts import render
from django.http import HttpResponse
from .models import Note

# Create your views here.
def pages_view(request):
    notes = Note.objects.all()
    return render(request, "pages/home.html", {
        "notes": notes
    })
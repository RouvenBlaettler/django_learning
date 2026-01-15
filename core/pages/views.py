from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import Note
from .forms import NoteForm

# Create your views here.
def pages_view(request):
    notes = Note.objects.all()

    if request.method == "POST":
        form = NoteForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('home')
    else:
        form = NoteForm()

    return render(request, "pages/home.html", {
        "notes": notes,
        "form" : form
    })
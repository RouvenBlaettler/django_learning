from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from .models import Note
from .forms import NoteForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.db.models import Q

@login_required
def delete_note(request, note_id):
    note = get_object_or_404(Note, id=note_id, user=request.user)
    if request.method == "POST":
        note.delete()
        messages.success(request, "Note deleted successfully.")
        return redirect('home')
    return render(request, "pages/delete_note.html", {
        "note": note
    })



def edit_note(request, note_id):
    note = get_object_or_404(Note, id=note_id, user=request.user)
    if request.method == "POST":
        form = NoteForm(request.POST, instance=note)
        if form.is_valid():
            form.save()
            messages.success(request, "Note updated successfully.")
            return redirect('home')
    else:
        form = NoteForm(instance=note)

    return render(request, "pages/edit_note.html", {
        "form": form
    })

def pages_view(request):
    if not request.user.is_authenticated:
        return redirect('login')
    
    query = request.GET.get('q')

    notes = Note.objects.filter(user=request.user)

    if query:
        notes = notes.filter(
            Q(title__icontains=query) | Q(content__icontains=query)
        )


    if request.method == "POST":
        form = NoteForm(request.POST)
        if form.is_valid():
            note = form.save(commit=False)
            note.user = request.user
            note.save()
            messages.success(request, "Note added successfully.")
            return redirect('home')
    else:
        form = NoteForm()

    return render(request, "pages/home.html", {
        "notes": notes,
        "form" : form
    })


def register_view(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = UserCreationForm()
    
    return render(request, "pages/register.html", {
        "form": form
    })

def login_view(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            return redirect('home')
        else:
            return render(request, "pages/login.html")
    return render(request, "pages/login.html")

def logout_view(request):
    logout(request)
    return redirect('login')
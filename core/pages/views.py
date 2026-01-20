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
    """Delete a specific note owned by the current user.
    
    Requires login. Only allows deletion of notes belonging to the authenticated user.
    Shows confirmation page on GET, performs deletion on POST.
    """
    note = get_object_or_404(Note, id=note_id, user=request.user)
    if request.method == "POST":
        note.delete()
        messages.success(request, "Note deleted successfully.")
        return redirect('home')
    return render(request, "pages/delete_note.html", {
        "note": note
    })



def edit_note(request, note_id):
    """Edit an existing note owned by the current user.
    
    Retrieves the note by ID and ensures it belongs to the authenticated user.
    On GET: displays pre-filled form with current note data.
    On POST: validates and saves the updated note.
    """
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
    """Main home page view - displays all notes and allows creating new ones.
    
    Features:
    - Redirects unauthenticated users to login page
    - Displays notes belonging to the current user
    - Supports search filtering via 'q' query parameter (searches title and content)
    - On POST: creates a new note associated with the current user
    - On GET: displays all notes and empty form
    """
    # Redirect unauthenticated users to login
    if not request.user.is_authenticated:
        return redirect('login')
    
    # Get search query from URL parameters
    query = request.GET.get('q')

    # Filter notes to show only those belonging to the current user
    notes = Note.objects.filter(user=request.user)

    # If search query exists, filter by title or content (case-insensitive)
    if query:
        notes = notes.filter(
            Q(title__icontains=query) | Q(content__icontains=query)
        )

    # Handle note creation via POST request
    if request.method == "POST":
        form = NoteForm(request.POST)
        if form.is_valid():
            note = form.save(commit=False)  # Don't save yet
            note.user = request.user  # Associate note with current user
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
    """Handle user registration.
    
    On GET: displays empty registration form.
    On POST: validates form and creates new user account, then redirects to login.
    Uses Django's built-in UserCreationForm for user creation.
    """
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()  # Create new user
            return redirect('login')
    else:
        form = UserCreationForm()
    
    return render(request, "pages/register.html", {
        "form": form
    })

def login_view(request):
    """Handle user authentication and login.
    
    On GET: displays login form.
    On POST: authenticates user with provided credentials.
    - If authentication succeeds: logs in user and redirects to home page.
    - If authentication fails: re-displays login form.
    """
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)  # Create session for authenticated user
            return redirect('home')
        else:
            return render(request, "pages/login.html")  # Show login form again on failure
    return render(request, "pages/login.html")

def logout_view(request):
    """Log out the current user and redirect to login page.
    
    Clears the user's session and redirects to the login page.
    """
    logout(request)  # End the user's session
    return redirect('login')
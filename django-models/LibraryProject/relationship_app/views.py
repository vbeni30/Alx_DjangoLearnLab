from django.shortcuts import render
from .models import Book
from .models import Library
from django.views.generic.detail import DetailView

# Function-based view
def list_books(request):
    books = Book.objects.all()
    # The path MUST be 'relationship_app/list_books.html'
    return render(request, 'relationship_app/list_books.html', {'books': books})

# Class-based view
class LibraryDetailView(DetailView):
    model = Library
    # The path MUST be 'relationship_app/library_detail.html'
    template_name = 'relationship_app/library_detail.html'
    context_object_name = 'library'

def home_view(request):
    return render(request, 'relationship_app/home.html')

from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login

def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('list_books') # Redirect to a page after registration
    else:
        form = UserCreationForm()
    return render(request, 'relationship_app/register.html', {'form': form})
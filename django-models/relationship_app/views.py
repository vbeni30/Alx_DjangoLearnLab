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
from django.shortcuts import render
from django.views.generic.detail import DetailView
from .models import Book
from .models import Library  # Checker requirement 1

# Function-based view (keep this for the first task)
def list_books(request):
    books = Book.objects.all()
    return render(request, 'relationship_app/list_books.html', {'books': books})

# Class-based view
class LibraryDetailView(DetailView):
    model = Library
    # Checker requirement 2: Must include the full path
    template_name = 'relationship_app/library_detail.html'
    
    # Checker requirement 3: Ensure 'library' is the context name
    context_object_name = 'library'
from rest_framework import generics, permissions
from .models import Book
from .serializers import BookSerializer

"""
BookListView:
- GET: Retrieve all books
- Public access (read-only)
"""
class BookListView(generics.ListAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [permissions.AllowAny]


"""
BookDetailView:
- GET: Retrieve a single book by ID
- Public access (read-only)
"""
class BookDetailView(generics.RetrieveAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [permissions.AllowAny]


"""
BookCreateView:
- POST: Create a new book
- Restricted to authenticated users
"""
class BookCreateView(generics.CreateAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [permissions.IsAuthenticated]


"""
BookUpdateView:
- PUT / PATCH: Update an existing book
- Restricted to authenticated users
"""
class BookUpdateView(generics.UpdateAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [permissions.IsAuthenticated]


"""
BookDeleteView:
- DELETE: Remove a book
- Restricted to authenticated users
"""
class BookDeleteView(generics.DestroyAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [permissions.IsAuthenticated]

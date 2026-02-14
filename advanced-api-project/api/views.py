from rest_framework import generics, filters
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated
from django_filters import rest_framework
from django_filters.rest_framework import DjangoFilterBackend
from .models import Book
from .serializers import BookSerializer

"""
BookListView:
- GET /api/books/
- Retrieve all books with filtering, search, and ordering
- Public read access
Query Params:
    ?title=<title>               # filter by title exact match
    ?author__name=<author_name>  # filter by author name
    ?publication_year=<year>     # filter by year
    ?search=<text>               # search title or author
    ?ordering=title              # ordering by title
    ?ordering=-publication_year  # descending order
"""
class BookListView(generics.ListAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    # Filtering + Search + Ordering
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    
    # Fields available for filtering
    filterset_fields = ['title', 'author__name', 'publication_year']

    # Fields available for search
    search_fields = ['title', 'author__name']

    # Fields allowed for ordering
    ordering_fields = ['title', 'publication_year']
    ordering = ['title']  # default ordering


"""
BookDetailView:
- GET: Retrieve a single book
- Public read access
"""
class BookDetailView(generics.RetrieveAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]


"""
BookCreateView:
- POST: Create a new book
- Authenticated users only
"""
class BookCreateView(generics.CreateAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [IsAuthenticated]


"""
BookUpdateView:
- PUT / PATCH: Update a book
- Authenticated users only
"""
class BookUpdateView(generics.UpdateAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [IsAuthenticated]


"""
BookDeleteView:
- DELETE: Remove a book
- Authenticated users only
"""
class BookDeleteView(generics.DestroyAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [IsAuthenticated]

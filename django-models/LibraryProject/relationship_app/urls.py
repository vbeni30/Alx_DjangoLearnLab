from django.urls import path
from .views import list_books, LibraryDetailView, home_view # Add home_view here

urlpatterns = [
    path('', home_view, name='home'), # This maps the root URL
    path('books/', list_books, name='list_books'),
    path('library/<int:pk>/', LibraryDetailView.as_view(), name='library_detail'),
]
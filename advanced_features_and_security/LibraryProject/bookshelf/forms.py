from django import forms
from .models import Book

# Example form for the Book model
class ExampleForm(forms.ModelForm):
    class Meta:
        model = Book
        fields = ['title', 'author', 'publication_year']

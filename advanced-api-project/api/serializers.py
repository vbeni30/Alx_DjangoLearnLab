from rest_framework import serializers
from datetime import date
from .models import Author, Book

"""
Serializers for the API application.

This module defines how model instances are converted to JSON
and vice versa, including validation and nested relationships.
"""


class BookSerializer(serializers.ModelSerializer):
    """
    Serializer for the Book model.

    Serializes all fields of the Book model.
    Includes custom validation to ensure the publication year
    is not set in the future.
    """

    class Meta:
        model = Book
        fields = '__all__'

    def validate_publication_year(self, value):
        """
        Custom validation method.

        Ensures the publication year is not in the future.
        """
        current_year = date.today().year
        if value > current_year:
            raise serializers.ValidationError(
                "Publication year cannot be in the future."
            )
        return value


class AuthorSerializer(serializers.ModelSerializer):
    """
    Serializer for the Author model.

    Includes:
    - name field
    - nested list of related books using BookSerializer

    The 'books' field dynamically serializes all books
    related to the author using the related_name defined
    in the Book model.
    """
    books = BookSerializer(many=True, read_only=True)

    class Meta:
        model = Author
        fields = ['id', 'name', 'books']

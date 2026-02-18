from django.db import models


class Author(models.Model):
    """
    Author model represents a book author.

    Fields:
    - name: Stores the author's full name.

    Relationship:
    - One Author can have many Books (one-to-many relationship).
    """

    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class Book(models.Model):
    """
    Book model represents a book written by an author.

    Fields:
    - title: Title of the book.
    - publication_year: Year the book was published.
    - author: ForeignKey linking the book to its author.

    Relationship:
    - Each Book belongs to one Author.
    """

    title = models.CharField(max_length=255)
    publication_year = models.IntegerField()
    author = models.ForeignKey(
        Author,
        related_name='books',
        on_delete=models.CASCADE
    )

    def __str__(self):
        return self.title

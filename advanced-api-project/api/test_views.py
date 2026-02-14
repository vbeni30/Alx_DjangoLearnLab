from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from django.contrib.auth.models import User
from .models import Author, Book

class BookAPITestCase(APITestCase):
    def setUp(self):
        """
        Set up test data and test user.
        """
        # Create test user
        self.user = User.objects.create_user(username="testuser", password="password123")

        # Create authors
        self.author1 = Author.objects.create(name="Author One")
        self.author2 = Author.objects.create(name="Author Two")

        # Create books
        self.book1 = Book.objects.create(title="Book One", publication_year=2000, author=self.author1)
        self.book2 = Book.objects.create(title="Book Two", publication_year=2010, author=self.author2)

    def test_list_books(self):
        """
        Test GET /books/ (list) endpoint
        """
        url = reverse("book-list")
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)

    def test_create_book_authenticated(self):
        """
        Test POST /books/ with authenticated user
        """
        self.client.login(username="testuser", password="password123")
        url = reverse("book-create")
        data = {
            "title": "Book Three",
            "publication_year": 2023,
            "author": self.author1.id
        }
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Book.objects.count(), 3)
        self.assertEqual(Book.objects.last().title, "Book Three")

    def test_create_book_unauthenticated(self):
        """
        Test POST /books/ with unauthenticated user should fail
        """
        url = reverse("book-create")
        data = {
            "title": "Book Three",
            "publication_year": 2023,
            "author": self.author1.id
        }
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_update_book_authenticated(self):
        """
        Test PUT /books/<id>/ with authenticated user
        """
        self.client.login(username="testuser", password="password123")
        url = reverse("book-update", args=[self.book1.id])
        data = {
            "title": "Updated Book One",
            "publication_year": 2001,
            "author": self.author1.id
        }
        response = self.client.put(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.book1.refresh_from_db()
        self.assertEqual(self.book1.title, "Updated Book One")

    def test_delete_book_authenticated(self):
        """
        Test DELETE /books/<id>/ with authenticated user
        """
        self.client.login(username="testuser", password="password123")
        url = reverse("book-delete", args=[self.book2.id])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Book.objects.count(), 1)

    def test_filter_books_by_title(self):
        """
        Test filtering books by title
        """
        url = reverse("book-list") + "?title=Book One"
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]["title"], "Book One")

    def test_search_books_by_author(self):
        """
        Test searching books by author name
        """
        url = reverse("book-list") + "?search=Author Two"
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]["author"], self.author2.id)

    def test_order_books_by_publication_year(self):
        """
        Test ordering books by publication_year descending
        """
        url = reverse("book-list") + "?ordering=-publication_year"
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data[0]["publication_year"], 2010)

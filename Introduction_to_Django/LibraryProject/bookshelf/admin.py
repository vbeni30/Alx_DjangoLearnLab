from django.contrib import admin
from .models import Book

# Basic registration
# admin.site.register(Book)

# Customized admin for Book
@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'publication_year')  # columns to show
    search_fields = ('title', 'author')                     # enable search
    list_filter = ('publication_year',)                     # add filter by year

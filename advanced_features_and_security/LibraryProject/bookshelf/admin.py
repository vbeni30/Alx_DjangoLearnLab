from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Book, CustomUser  # Ensure both are imported

# Register the Book model
admin.site.register(Book)

# Register the CustomUser model
class CustomUserAdmin(UserAdmin):
    model = CustomUser
    fieldsets = UserAdmin.fieldsets + (
        (None, {'fields': ('date_of_birth', 'profile_photo')}),
    )
    add_fieldsets = UserAdmin.add_fieldsets + (
        (None, {'fields': ('date_of_birth', 'profile_photo')}),
    )

admin.site.register(CustomUser, CustomUserAdmin)
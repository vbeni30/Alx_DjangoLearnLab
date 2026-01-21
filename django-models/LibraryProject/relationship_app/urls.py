from django.urls import path
from . import views
from django.contrib.auth import views as auth_views
from .views import admin_view, librarian_view, member_view # Import specific role views

urlpatterns = [
    path('books/', views.list_books, name='list_books'),
    path('library/<int:pk>/', views.LibraryDetailView.as_view(), name='library_detail'),
    
    # Role-based paths
    # Note: Use 'admin/' or 'admin_view/' based on your preference, 
    # but 'admin/' is standard. The "name" must be 'admin_view'.
    path('admin/', views.admin_view, name='admin_view'),
    path('librarian/', views.librarian_view, name='librarian_view'),
    path('member/', views.member_view, name='member_view'),
    
    # Authentication URLs
    path('login/', auth_views.LoginView.as_view(template_name='relationship_app/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(template_name='relationship_app/logout.html'), name='logout'),
    path('register/', views.register, name='register'),
]
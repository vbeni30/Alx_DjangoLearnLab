from django.urls import path
from . import views
from django.contrib.auth import views as auth_views # Use this alias

urlpatterns = [
    path('books/', views.list_books, name='list_books'),
    path('library/<int:pk>/', views.LibraryDetailView.as_view(), name='library_detail'),
    
    # Use auth_views for login and logout
    path('login/', auth_views.LoginView.as_view(template_name='relationship_app/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(template_name='relationship_app/logout.html'), name='logout'),
    
    # Use the function-based view for registration
    path('register/', views.register, name='register'),
]
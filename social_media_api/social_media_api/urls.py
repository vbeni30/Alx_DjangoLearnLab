from django.contrib import admin
from django.urls import path, include

import posts.urls  

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('accounts.urls')),
    path('api/', include('posts.urls')),
    path('api/', include('notifications.urls')),
]

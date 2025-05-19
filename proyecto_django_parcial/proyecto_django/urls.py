from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('applications.core.urls')),
    path('games/', include('applications.games.urls')),
    path('profiles/', include('applications.profiles.urls')),
    path('community/', include('applications.community.urls')),
    path('auth/', include('applications.auth.urls')),
]
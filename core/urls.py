from django.urls import path, include
from .views import home

urlpatterns = [
    path('', home, name='home'),  
    path('api/users/', include('users.urls')),  
    path('api/events/', include('music_events.urls')), 
]

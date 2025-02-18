from django.urls import path, include
from .views import HomeView, LoginView, RegisterView, LogoutView

urlpatterns = [
    path('', HomeView.as_view(), name='home'),  
    path('login/', LoginView.as_view(), name='login'),  
    path('register/', RegisterView.as_view(), name='register'),  
    path('logout/', LogoutView.as_view(), name='logout'),  
    path('api/users/', include('users.urls')),  
    path('api/events/', include('music_events.urls')), 
]

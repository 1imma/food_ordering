from django.urls import path
from .views import signup, login,logout,dashboard, edit_profile


urlpatterns = [
    path('signup/', signup, name='signup'),
    path('login/', login, name='login'),
    path('logout/', logout, name='logout'),
    path('dashboard/', dashboard, name='dashboard'),
    path('edit-profile/', edit_profile, name='edit_profile'),
]

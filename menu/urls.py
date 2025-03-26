from django.urls import path
from .views import menu_view

urlpatterns = [
    path('menu/', menu_view, name='menu'),  # Menu page URL
]

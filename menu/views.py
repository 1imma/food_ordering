from django.shortcuts import render
from .models import MenuItem  # Import MenuItem model

# Create your views here.
def menu_view(request):
    menu_items = MenuItem.objects.all()  # Fetch all menu items
    return render(request, 'menu.html', {'menu_items': menu_items})

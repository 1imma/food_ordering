from django.shortcuts import render
#landing page view

def landing(request):
    return render(request, 'landing.html')
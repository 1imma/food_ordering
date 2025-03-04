from django.shortcuts import render, redirect
from django.contrib import messages
from .models import User



# Signup view

def signup(request):
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']

        if User.objects.filter(username=username).exists:
            messages.error('Username taken')
            return redirect('signup')
        
        if User.objects.filter(email=email).exists:
            messages.error('Email is registered')
            return redirect('signup')

        user = User(username=username, email=email, password=password)
        user.save()

        messages.success('Created Account Successfully, please login')
        return redirect('login')
    return render(request, 'accounts/signup.html')


#login view

def login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        try:
            user = User.objects.get(username=username, password=password)
            request.session['user_id'] = user.id
            messages.success('login successfully')
            return redirect('dashboard')
        except User.DoesNotExist:
            messages.error('Invalid Username or Password')
            return redirect('login')
        
    return render(request, 'accounts/login.html')



from django.shortcuts import render, redirect
from django.contrib import messages
from .models import User
import hashlib



# Signup view

def signup(request):
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password1']
        confirm_password = request.POST['password2']

        if password != confirm_password:
            messages.error(request, "Passwords do not match!")
            return redirect('signup')

        if User.objects.filter(username=username).exists() or User.objects.filter(email=email).exists():
            messages.error(request,'Username or Email taken')
            return redirect('signup')
        
        """if User.objects.filter(email=email).exists:
            messages.error('Email is registered')
            return redirect('signup')"""

        # Hash the password before storing
        hashed_password = hashlib.sha256(password.encode()).hexdigest()
        user = User(username=username, email=email, password=hashed_password)
        user.save()

        messages.success(request, 'Created Account Successfully, please login')
        return redirect('login')
    return render(request, 'accounts/signup.html')


#login view

def login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        hashed_password = hashlib.sha256(password.encode()).hexdigest()

        try:
            user = User.objects.get(username=username, password=hashed_password)
            request.session['user_id'] = user.id #save the session
            messages.success(request,'login successfully')
            return redirect('dashboard')
        except User.DoesNotExist:
            messages.error(request,'Invalid Username or Password')
            return redirect('login')
        
    return render(request, 'accounts/login.html')

#logout view

def logout(request):
    request.session.flush()  # Clear session
    messages.success(request, "Logged out successfully!")
    return redirect('login')

#dashboard view

def dashboard(request):
    if 'user_id' not in request.session:
        messages.error(request, 'You must be logged in to access the dashboard!')
        return redirect('login')
    user = User.objects.get(id=request.session['user_id'])
    return render(request, 'accounts/dashboard.html',{"user":user})


#edit profile view

def edit_profile(request):
    if 'user_id' not in request.session:
        messages.error(request, 'You must be logged in!')
        return redirect('login')

    user = User.objects.get(id=request.session['user_id'])

    if request.method == 'POST':
        user.phone_number = request.POST.get('phone_number', user.phone_number)
        user.address = request.POST.get('address', user.address)
        user.save()

        messages.success(request, "Profile updated successfully!")
        return redirect('dashboard')
    
    return render(request, 'accounts/edit_profile.html', {'user':user})





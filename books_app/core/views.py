from django.shortcuts import render, redirect


def landing(request):
    """Render the landing page"""
    return render(request, 'landing.html')


def home(request):
    """Render the home page"""
    if not request.user.is_authenticated:
        return redirect('/login')

    return render(request, 'home.html')


def login(request):
    """Render the login page"""
    if request.user.is_authenticated:
        return redirect('/home')

    return render(request, 'login.html')


def register(request):
    """Render the register page"""
    if request.user.is_authenticated:
        return redirect('/home')

    return render(request, 'register.html')

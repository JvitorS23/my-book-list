from django.shortcuts import render


def landing(request):
    """Render the landing page"""
    return render(request, 'landing.html')


def home(request):
    """Render the home page"""
    if request.user.is_authenticated:
        print("Logged in")
    else:
        print("Not logged in")

    return render(request, 'home.html')


def login(request):
    """Render the login page"""
    if request.user.is_authenticated:
        print("Logged in")
    else:
        print("Not logged in")

    return render(request, 'login.html')


def register(request):
    """Render the register page"""
    if request.user.is_authenticated:
        print("Logged in")
    else:
        print("Not logged in")

    return render(request, 'register.html')

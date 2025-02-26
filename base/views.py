from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
from .models import Voter, Candidate
from django.contrib.auth.models import User
from django.contrib.auth.views import LoginView, FormView
from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse_lazy


# Create your views here.
def home(request):
    return render(request, 'base/home.html')



def login_view(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)
        if user is None:
            messages.error(request, 'user does not exist')
            return redirect('login_view')
        elif user:
            login(request, user)
            messages.success(request, 'Login successful')
            return redirect('home')
        else:
            messages.error(request, 'Invalid username or password')
            return redirect('login_view')

    return render(request, 'base/login.html')



def register(request):
    if request.method == "POST":
        email = request.POST.get("email")
        username = request.POST.get("username")
        password1 = request.POST.get("password1")
        password2 = request.POST.get("password2")

        if not email:
            messages.error(request, "email is required.")
            return redirect("register")
        
        if not username:
            messages.error(request, "registration number is required.")
            return redirect("register")


        if password1 != password2:
            messages.error(request, "Passwords do not match.")
            return redirect("register")

        if User.objects.filter(username=username).exists():
            messages.error(request, "Student with that registration number already exists, continue to login.")
            return redirect("register")

        user = User.objects.create_user(username=username, email=email, password=password1)
        user.save()
        
        messages.success(request, "Account created successfully. Please log in.")
        return redirect("login_view")

    return render(request, "base/register.html")

    
def logout_view(request):
    logout(request)
    messages.success(request, "You have been logged out.")
    return redirect('login_view')

def voting_view(request):
    candidates = Candidate.objects.all()
    context = {'candidates':candidates}
    return render(request, 'base/vote.html', context)
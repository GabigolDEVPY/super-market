from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect
from .forms import RegisterForm

def logout_user(request):
    if request.method == "POST":
        logout(request)
        return redirect("market:login")
    return redirect("market:home")
        

def register_user(request):
    if request.method == "GET":
        form = RegisterForm()
        return render(request, "register.html", {"form": form})
    form = RegisterForm(request.POST)
    if form.is_valid():
        form.save()
        return redirect("market:login")  
    return render(request, "register.html", {"form": form})
    

def login_user(request):
    if request.method == "GET":
        return render(request, "login.html")
    
    username = request.POST.get("username") 
    password = request.POST.get("password")
    
    user = authenticate(request, username=username, password=password)
    if user is not None:
        login(request, user)
        return redirect("market:home")   
    else:
        return redirect("market:login")
    
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect
from django.contrib import messages
from django.http import JsonResponse

def logout_user(request):
    if request.method == "POST":
        logout(request)
        return redirect("market:login")
    else:
        return redirect("market:home")
        

def register_user(request):
    if request.method == "GET":
        return render(request, "register.html")
    username = request.POST.get("username")
    password = request.POST.get("password")
    email = request.POST.get("email")
    
    if User.objects.filter(username=username).exists():
        return redirect("market:register")  
    else:
        User.objects.create_user(username=username, password=password, email=email)
        return redirect("market:login")  

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
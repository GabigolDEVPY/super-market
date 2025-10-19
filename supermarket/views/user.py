from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.contrib import messages
from django.http import JsonResponse

def register_user(request):
    if request.method == "GET":
        return render(request, "register.html")
    username = request.POST.get("username")
    password = request.POST.get("password")
    email = request.POST.get("email")
    
    if User.objects.filter(username=username).exists():
        messages.error(request, "User already exists!")
    else:
        User.objects.create_user(username=username, password=password, email=email)
        messages.success(request, "Usuário criado com sucesso!")
        return redirect("login")  # ou qualquer página que queira
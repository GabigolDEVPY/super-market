from django.shortcuts import render, redirect
from django.http import request, JsonResponse

# Create your views here.
def home(request):
    return render(request ,"home.html")
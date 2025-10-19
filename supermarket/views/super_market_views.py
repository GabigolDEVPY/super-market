from django.shortcuts import render, redirect
from django.http import request, JsonResponse
from django.contrib.auth.decorators import login_required

# Create your views here.

@login_required(login_url='market:login')
def home(request):
    return render(request ,"home.html")
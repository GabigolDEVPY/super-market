from django.shortcuts import render, redirect
from django.http import request, JsonResponse

# Create your views here.
def home(request):
    return JsonResponse({"nome": "gabriel"}, safe=False)
    # return render(request ,"home.html")
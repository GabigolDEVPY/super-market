from django.shortcuts import render
from django.views import View
from django.contrib.auth import authenticate, login, logout
from django.urls import reverse_lazy
from django.shortcuts import render, redirect
from django.views.generic import FormView
from .forms import RegisterForm


class LogoutView(View):
    def post(self, request):
        logout(request)
        return redirect("accounts:login")
    def get(self, request):
        return redirect("market:home")

class LoginView(View):
    def get(self, request):
        return render(request, "login.html", {"hide_navbar": True})

    def post(self, request):
        username = request.POST.get("username")
        password = request.POST.get("password")
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect("market:home")
        return redirect("accounts:login")
        
        
class RegisterView(FormView):
    template_name = "register.html"
    form_class = RegisterForm
    success_url = reverse_lazy("accounts:login")
    extra_context = {"hide_navbar": True}
    
    
    def form_valid(self, form):
        form.save()
        return super().form_valid(form)
    

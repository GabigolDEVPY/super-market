from django.contrib import messages
from django.shortcuts import render
from django.views import View
from django.contrib.auth import authenticate, login, logout
from django.urls import reverse_lazy
from django.shortcuts import render, redirect
from django.views.generic import FormView
from django.contrib.auth.mixins import LoginRequiredMixin
from .utils import add_cep, validade_cep
from .forms import RegisterForm
from cart.views import CartView


class LogoutView(View):
    def post(self, request):
        logout(request)
        return redirect("accounts:login")
    def get(self, request):
        return redirect("market:home")

class LoginView(View):
    def get(self, request):
        return render(request, "accounts/login.html", {"hide_navbar": True})

    def post(self, request):
        username = request.POST.get("username")
        password = request.POST.get("password")
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect("market:home")
        messages.error(request, "Username or password expired")
        return redirect("accounts:login")
        
        
class RegisterView(FormView):
    template_name = "register.html"
    form_class = RegisterForm
    success_url = reverse_lazy("accounts:login")
    extra_context = {"hide_navbar": True}
    
    
    def form_valid(self, form):
        form.save()
        return super().form_valid(form)
    

class AddAdress(View, LoginRequiredMixin):
    def post(self, request):
        cep = request.POST.get("cep")
        if cep:
            response = validade_cep(cep)
            if response == "Error":
                messages.error(request, "Cep Inválido", extra_tags="open_modal")
            elif response == "Timeout":
                messages.error(request, "O servidor demorou muito!", extra_tags="open_modal")
            form, error = add_cep(request)
            if error:
                messages.error(request, "Corrija os erros do endereço", extra_tags="open_modal")
                return CartView.as_view()(request, form=form)
            return redirect("cart:cart")
        messages.error(request, "Insira o CEP", extra_tags="open_modal")
        return redirect("cart:cart")
        

class Home(LoginRequiredMixin, View):
    def get(self, request):
        print("chegou aqui karalhooooo")
        return render(request, "accounts/home.html")
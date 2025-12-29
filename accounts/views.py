from urllib import request
from django.contrib import messages
from django.shortcuts import get_object_or_404, render
from django.views import View
from django.contrib.auth import authenticate, login, logout
from django.urls import reverse_lazy
from django.shortcuts import render, redirect
from django.views.generic import FormView, TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from accounts.models import Address
from .utils import add_cep, validade_cep, create_inventory_and_cart
from .forms import RegisterForm, AdressForm
from accounts.states import states


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
        messages.error(request, "Username or password expired", extra_tags="login_message")
        return redirect("accounts:login")
        
        
class RegisterView(FormView):
    template_name = "accounts/register.html"
    form_class = RegisterForm
    success_url = reverse_lazy("accounts:login")
    extra_context = {"hide_navbar": True}
    
    
    def form_valid(self, form):
        user = form.save(commit=False)
        user.save()
        create_inventory_and_cart(user)
        return super().form_valid(form)
    

class AddAdress(LoginRequiredMixin, View):
    def get(self, request):
        return redirect("accounts:home")
    
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
                messages.error(request, error, extra_tags="open_modal")
            return redirect("accounts:home")
        messages.error(request, "Insira o CEP", extra_tags="open_modal")
        return redirect("home")
        

class Home(LoginRequiredMixin, TemplateView):
    template_name = "accounts/home.html"
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["form"] = AdressForm()
        context["states"] = states
        context["address"] = self.request.user.address.all()
        return context

class DeleteAddress(LoginRequiredMixin, View):
    def post(self, request):
        user = request.POST.get("user")
        name = request.POST.get("name")
        address = get_object_or_404(Address, user=user, name=name)
        address.delete()
        return redirect("accounts:home")
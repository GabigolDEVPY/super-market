from django.contrib import messages
from django.views import View
from django.contrib.auth import authenticate, login, logout
from django.urls import reverse_lazy
from django.core.exceptions import ValidationError
from django.shortcuts import render, redirect
from django.views.generic import FormView, TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from .services import User
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
        error = User.user_login(request)
        if error:
            messages.error(request, "Username or password expired", extra_tags="login_message")
            return redirect("accounts:login")
        return redirect("market:home")
        
        
class RegisterView(FormView):
    template_name = "accounts/register.html"
    form_class = RegisterForm
    success_url = reverse_lazy("accounts:login")
    extra_context = {"hide_navbar": True}
    
    def form_valid(self, form):
        User.user_register(form)
        return super().form_valid(form)
    

class AddAdress(LoginRequiredMixin, View):
    def get(self, request):
        return redirect("accounts:home")
    
    def post(self, request):
        try:
            User.create_address(request.user, request.POST) 
        except ValidationError as e:
            messages.error(request, e.message, extra_tags="addressModal")
            return redirect('accounts:home')
        


class Home(LoginRequiredMixin, TemplateView):
    template_name = "accounts/home.html"
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["form"] = AdressForm()
        context["states"] = states
        context["address"] = self.request.user.address.all()
        context["orders"] = User.get_orders(self.request)
        return context


class DeleteAddress(LoginRequiredMixin, View):
    def post(self, request):
        User.delete_address(request)
        return redirect("accounts:home")


class ChangePassword(LoginRequiredMixin, View):
    def post(self, request):
        result = User.change_password(request)
        if result:
            messages.error(request, "Senha atual incorreta", extra_tags="passwordModal")
            return redirect("accounts:home")
        messages.success(request, "Senha alterada com sucesso. Faça login novamente", extra_tags="passwordModal")
        return redirect("accounts:login")
    
    
class ChangeEmail(LoginRequiredMixin, View):
    def post(self, request):
        response = User.change_email(request)
        if response:
            messages.error(request, "Informe um e-mail.", extra_tags="emailModal")
            return redirect("accounts:home")
        messages.success(request, "E-mail atualizado com sucesso", extra_tags="emailModal")
        return redirect("accounts:home")
        
        
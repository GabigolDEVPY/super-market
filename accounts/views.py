from django.contrib import messages
from django.views import View
from django.contrib.auth import logout
from django.urls import reverse_lazy
from django.core.exceptions import ValidationError, ObjectDoesNotExist
from django.shortcuts import render, redirect
from django.views.generic import FormView, TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from .services import AddressService, UserService, AuthService
from .forms import RegisterForm, AdressForm
from accounts.states import states


class LogoutView(View):
    def get(self, request):
        return redirect("market:home")
    def post(self, request):
        logout(request)
        return redirect("accounts:login")


class LoginView(View):
    def get(self, request):
        return render(request, "accounts/login.html", {"hide_navbar": True})

    def post(self, request):
        try:
            AuthService.user_login(request, username=request.POST.get("username"), password=request.POST.get("password"))
            return redirect("market:home")
        except ValidationError as e:
            messages.error(request, e.message, extra_tags="login_message")
            return redirect("accounts:login")
        
        
class RegisterView(FormView):
    template_name = "accounts/register.html"
    form_class = RegisterForm
    success_url = reverse_lazy("accounts:login")
    extra_context = {"hide_navbar": True}
    
    def form_valid(self, form):
        UserService.user_register(form)
        return super().form_valid(form)
    

class AddAdress(LoginRequiredMixin, View):
    def get(self, request):
        return redirect("accounts:home")
    
    def post(self, request):
        try:
            AddressService.create_address(request.user, request.POST)
            return redirect('accounts:home') 
        except ValidationError as e:
            messages.error(request, e.messages[0], extra_tags="addressModal")
            return redirect('accounts:home')
        


class Home(LoginRequiredMixin, TemplateView):
    template_name = "accounts/home.html"
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["form"] = AdressForm()
        context["states"] = states
        context["address"] = self.request.user.address.all()
        context["orders"] = UserService.get_orders(self.request)
        return context


class DeleteAddress(LoginRequiredMixin, View):
    def post(self, request):
        try:
            AddressService.delete_address(request.user, request.POST.get("name"))
        except ObjectDoesNotExist:  
            messages.error(request, "objeto não existe", extra_tags="generic")
        return redirect("accounts:home")


class ChangePassword(LoginRequiredMixin, View):
    def post(self, request):
        try:
            AuthService.change_password(request.user, request.POST.get("old_password"), request.POST.get("new_password"))
            messages.success(request, "Senha alterada com sucesso. Faça login novamente", extra_tags="passwordModal")
            return redirect("accounts:login")
        except ValidationError as e:
            messages.error(request, e.messages[0], extra_tags="passwordModal")
            return redirect("accounts:home")
            
    
class ChangeEmail(LoginRequiredMixin, View):
    def post(self, request):
        if not request.POST.get("email"):
            messages.error(request, "Informe um e-mail.", extra_tags="emailModal")
            return redirect("accounts:home")
        UserService.change_email(email=request.POST.get("email"), user=request.user)
        messages.success(request, "E-mail atualizado com sucesso", extra_tags="emailModal")
        return redirect("accounts:home")
        
        
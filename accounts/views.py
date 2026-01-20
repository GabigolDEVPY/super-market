from django.contrib import messages
from django.views import View
from django.contrib.auth import authenticate, login, logout
from django.urls import reverse_lazy
from django.shortcuts import render, redirect
from django.views.generic import FormView, TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from .services import user
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
        error = user.add_address(request) 
        if error:
            messages.error(request, error, extra_tags="addressModal")
            return redirect('accounts:home')
        
        messages.success(request, "Endereço adicionado com sucesso!")
        return redirect("accounts:home")


class Home(LoginRequiredMixin, TemplateView):
    template_name = "accounts/home.html"
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["form"] = AdressForm()
        context["states"] = states
        context["address"] = self.request.user.address.all()
        context["orders"] = user.get_orders(self.request)
        return context

class DeleteAddress(LoginRequiredMixin, View):
    def post(self, request):
        user.delete_address(request)
        return redirect("accounts:home")

class ChangePassword(LoginRequiredMixin, View):
    def post(self, request):
        user = request.user
        old_password = request.POST.get("old_password")
        new_password = request.POST.get("new_password")

        if not user.check_password(old_password):
            messages.error(request, "Senha atual incorreta", extra_tags="passwordModal")
            return redirect("accounts:home")
        user.set_password(new_password)
        user.save()
        
        messages.success(request, "Senha alterada com sucesso. Faça login novamente", extra_tags="passwordModal")
        return redirect("accounts:login")
    
class ChangeEmail(LoginRequiredMixin, View):
    def post(self, request):
        new_email = request.POST.get("email")
        
        if not new_email:
            messages.error(request, "Informe um e-mail.", extra_tags="emailModal")
            return redirect("accounts:home")
        
        request.user.email = new_email
        request.user.save()
        
        print("chegou aqui")
        messages.success(request, "E-mail atualizado com sucesso", extra_tags="emailModal")
        return redirect("accounts:home")
        
        
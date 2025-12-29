from django.urls import path
from . import views


app_name = 'accounts'

urlpatterns = [
    path("home/", views.Home.as_view(), name="home"),
    path("login/", views.LoginView.as_view(), name='login'),
    path("register/", views.RegisterView.as_view(), name='register'),
    path("logout/", views.LogoutView.as_view(), name="logout"),
    path("address/add/", views.AddAdress.as_view(), name="addaddress"),
    path("address/delete/", views.DeleteAddress.as_view(), name="deleteaddress")
]
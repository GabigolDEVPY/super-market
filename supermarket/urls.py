from django import views
from django.urls import path
from supermarket import views

app_name = 'market'

urlpatterns = [
    # home
    path("", views.HomeView.as_view(), name='home'),
    path("all/", views.AllProducts.as_view(), name='all'),
    path("search/", views.SearchProduct.as_view(), name='search'),
]

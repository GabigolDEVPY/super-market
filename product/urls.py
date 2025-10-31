from django import views
from django.urls import path
from . import views


app_name = 'product'

urlpatterns = [
    # product.views
    path("<int:id>/", views.product, name='product'),
    path("buy/<int:id>/", views.buynow, name='buynow'),
    path("buy/", views.productbuynow, name='productbuynow'),

]
from django import views
from django.urls import path
from . import views


app_name = 'product'

urlpatterns = [
    # product.views
    path("product/<int:id>/", views.product, name='product'),
    path("product/buy/<int:id>/", views.buynow, name='buynow'),
    path("product/buy", views.productbuynow, name='productbuynow'),

]
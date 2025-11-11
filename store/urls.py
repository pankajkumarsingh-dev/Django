from django.urls import path
from . import views

urlpatterns = [
    path('products/', views.product_list),
    path('products/<int:pk>/', views.product_detail),
    path('cart/', views.cart_detail),
    path('cart/add/', views.cart_add),
    path('cart/remove/', views.cart_remove),
]


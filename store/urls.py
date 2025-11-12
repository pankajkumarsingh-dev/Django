from django.urls import path
from . import views

urlpatterns = [
    path('register/', views.register_user),
    path('products/', views.product_list),
    path('products/<int:pk>/', views.product_detail),
    path('cart/', views.cart_detail),
    path('cart/add/', views.cart_add),
    path('cart/<int:pk>/update/', views.cart_update),
    path('cart/<int:pk>/remove/', views.cart_remove),
]

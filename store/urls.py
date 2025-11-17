from django.urls import path
from .views import (
    RegisterUserView,
    ProductListCreateView,
    ProductRetrieveUpdateDestroyView,
    CartView,
    CustomTokenObtainPairView
)

from rest_framework_simplejwt.views import TokenRefreshView



urlpatterns = [
    path('register/', RegisterUserView.as_view(),name='register'),
    path('login/', CustomTokenObtainPairView.as_view(),name='login'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

    path('products/', ProductListCreateView.as_view(),name='product-list'),
    path('products/<int:pk>/', ProductRetrieveUpdateDestroyView.as_view(),name='product-detail'),
    path('cart/', CartView.as_view(),name='cart-list-create'),
    # path('cart/add/', views.cart_add),
    path('cart/<int:pk>/update/', CartView.as_view(),name='cart-update-delete'),
    # path('cart/<int:pk>/remove/', views.cart_remove),
]

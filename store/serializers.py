from rest_framework import serializers
from .models import Product,CartItem
from django.contrib.auth.models import User

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'

class CartItemSerializer(serializers.ModelSerializer):
    product=ProductSerializer(read_only=True) 
    class Meta:
        model = CartItem
        fields = '__all__'


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True) # field should be used when deserializing, exlucde in serializing

    class Meta:
        model=User 
        fields = ['username','password']
    def create(self,validated_data):
        user = User.objects.create_user(
            username=validated_data['username'],
            password= validated_data['password']
        )

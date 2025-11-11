from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from .models import Product
from .serializers import ProductSerializer
from .cart import Cart

@api_view(['GET'])
def product_list(request):
    print("DEBUG: product_list called")
    products = Product.objects.all()
    serializer = ProductSerializer(products, many=True)
    return Response(serializer.data)

@api_view(['GET'])
def product_detail(request, pk):
    product = get_object_or_404(Product, pk=pk)
    serializer = ProductSerializer(product)
    return Response(serializer.data)

@api_view(['GET'])
def cart_detail(request):
    cart = Cart(request)
    return Response({
        'items': list(cart),
        'total': cart.total(),
    })

@api_view(['POST'])
def cart_add(request):
    cart = Cart(request)
    product_id = request.data.get('product_id')
    quantity = int(request.data.get('quantity', 1))
    product = get_object_or_404(Product, id=product_id)
    cart.add(product, quantity)
    return Response({'message': 'Added', 'cart': list(cart)}, status=status.HTTP_201_CREATED)

@api_view(['POST'])
def cart_remove(request):
    cart = Cart(request)
    product_id = request.data.get('product_id')
    product = get_object_or_404(Product, id=product_id)
    cart.remove(product)
    return Response({'message': 'Removed', 'cart': list(cart)})


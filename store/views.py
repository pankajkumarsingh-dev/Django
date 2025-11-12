from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import Product
from .models import CartItem
from .serializers import ProductSerializer,CartItemSerializer

from rest_framework.decorators import api_view, permission_classes
from django.shortcuts import get_object_or_404
from rest_framework.permissions import AllowAny
from django.contrib.auth.models import User
from django.http import HttpResponse
from http import HTTPStatus

from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.permissions import IsAuthenticated


# User Registration

@api_view(['POST'])
@permission_classes([AllowAny])
def register_user(request):
    username=request.data.get('username')
    password=request.data.get('password')
    if not username or not password:
        return Response({"error":'Please provide username and password'},status=status.HTTP_400_BAD_REQUEST)
    if User.objects.filter(username=username).exists():
        return Response({"error":'User already exists'},status=status.HTTP_400_BAD_REQUEST)
    user=User.objects.create_user(username=username,password=password)
    return Response({"msg":'successfully created'},status=status.HTTP_201_CREATED)


# Product Crud

@api_view(['GET','POST'])
@permission_classes([IsAuthenticatedOrReadOnly])
def product_list(request):
    if request.method=='GET':
        products=Product.objects.all()
        serializer=ProductSerializer(products,many=True)
        return Response(serializer.data)
    elif request.method=='POST':
        serializer=ProductSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data,status=status.HTTP_201_CREATED)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
    

@api_view(['GET','PUT','DELETE'])
@permission_classes([IsAuthenticatedOrReadOnly])
def product_detail(request,pk):
    product=get_object_or_404(Product,pk=pk)
    if request.method=='GET':
        serializer=ProductSerializer(product)
        return Response(serializer.data)

    elif request.method=='PUT':
        serializer=ProductSerializer(product,data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data,status=status.HTTP_200_OK)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)

    elif request.method=='DELETE':
        product.delete()
        return Response({"msg":'Deleted Successfully'},status=status.HTTP_204_NO_CONTENT)
    
# Cart Crud

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def cart_detail(request):
    items = CartItem.objects.filter(user=request.user)
    serializer = CartItemSerializer(items, many=True)
    total = sum(item.product.price * item.quantity for item in items)
    return Response({"items": serializer.data, "total": total}, status=status.HTTP_200_OK)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def cart_add(request):
    product_id = request.data.get('product_id')
    quantity = int(request.data.get('quantity', 1))
    product = get_object_or_404(Product, id=product_id)

    cart_item, created = CartItem.objects.get_or_create(
        user=request.user, product=product
    )
    if not created:
        cart_item.quantity += quantity
    else:
        cart_item.quantity = quantity

    cart_item.save()
    return Response({"msg": "Added successfully"}, status=status.HTTP_201_CREATED)


@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def cart_update(request, pk):
    cart_item = get_object_or_404(CartItem, id=pk, user=request.user)
    quantity = request.data.get('quantity')
    if quantity is not None:
        cart_item.quantity = int(quantity)
        cart_item.save()
    serializer = CartItemSerializer(cart_item)
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def cart_remove(request, pk):
    cart_item = get_object_or_404(CartItem, id=pk, user=request.user)
    cart_item.delete()
    return Response({"message": "Deleted successfully"}, status=status.HTTP_200_OK)








# @api_view(['GET'])
# def product_list(request):
#     print("DEBUG: product_list called")
#     products = Product.objects.all()
#     serializer = ProductSerializer(products, many=True)
#     return Response(serializer.data)

# @api_view(['GET'])
# def product_detail(request, pk):
#     product = get_object_or_404(Product, pk=pk)
#     serializer = ProductSerializer(product)
#     return Response(serializer.data)

# @api_view(['GET'])
# def cart_detail(request):
#     cart = Cart(request)
#     return Response({
#         'items': list(cart),
#         'total': cart.total(),
#     })

# @api_view(['POST'])
# def cart_add(request):
#     cart = Cart(request)
#     product_id = request.data.get('product_id')
#     quantity = int(request.data.get('quantity', 1))
#     product = get_object_or_404(Product, id=product_id)
#     cart.add(product, quantity)
#     return Response({'message': 'Added', 'cart': list(cart)}, status=status.HTTP_201_CREATED)

# @api_view(['POST'])
# def cart_remove(request):
#     cart = Cart(request)
#     product_id = request.data.get('product_id')
#     product = get_object_or_404(Product, id=product_id)
#     cart.remove(product)
#     return Response({'message': 'Removed', 'cart': list(cart)})





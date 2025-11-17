from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status,generics
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
from rest_framework.permissions import IsAuthenticated,AllowAny

from rest_framework_simplejwt.views import TokenObtainPairView
# from rest_framework_simplejwt.Tokens import RefreshToken
from rest_framework_simplejwt.tokens import RefreshToken

from rest_framework.response import Response
from rest_framework import status
from .models import UserSession


# # User Registration

# @api_view(['POST'])
# @permission_classes([AllowAny])
# def register_user(request):
#     username=request.data.get('username')
#     password=request.data.get('password')
#     if not username or not password:
#         return Response({"error":'Please provide username and password'},status=status.HTTP_400_BAD_REQUEST)
#     if User.objects.filter(username=username).exists():
#         return Response({"error":'User already exists'},status=status.HTTP_400_BAD_REQUEST)
#     user=User.objects.create_user(username=username,password=password)
#     return Response({"msg":'successfully created'},status=status.HTTP_201_CREATED)


# # Product Crud

# @api_view(['GET','POST'])
# @permission_classes([IsAuthenticatedOrReadOnly])
# def product_list(request):
#     if request.method=='GET':
#         products=Product.objects.all()
#         serializer=ProductSerializer(products,many=True)
#         return Response(serializer.data)
#     elif request.method=='POST':
#         serializer=ProductSerializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data,status=status.HTTP_201_CREATED)
#         return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
    

# @api_view(['GET','PUT','DELETE'])
# @permission_classes([IsAuthenticatedOrReadOnly])
# def product_detail(request,pk):
#     product=get_object_or_404(Product,pk=pk)
#     if request.method=='GET':
#         serializer=ProductSerializer(product)
#         return Response(serializer.data)

#     elif request.method=='PUT':
#         serializer=ProductSerializer(product,data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data,status=status.HTTP_200_OK)
#         return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)

#     elif request.method=='DELETE':
#         product.delete()
#         return Response({"msg":'Deleted Successfully'},status=status.HTTP_204_NO_CONTENT)
    
# # Cart Crud

# @api_view(['GET'])
# @permission_classes([IsAuthenticated])
# def cart_detail(request):
#     items = CartItem.objects.filter(user=request.user)
#     serializer = CartItemSerializer(items, many=True)
#     total = sum(item.product.price * item.quantity for item in items)
#     return Response({"items": serializer.data, "total": total}, status=status.HTTP_200_OK)


# @api_view(['POST'])
# @permission_classes([IsAuthenticated])
# def cart_add(request):
#     product_id = request.data.get('product_id')
#     quantity = int(request.data.get('quantity', 1))
#     product = get_object_or_404(Product, id=product_id)

#     cart_item, created = CartItem.objects.get_or_create(
#         user=request.user, product=product
#     )
#     if not created:
#         cart_item.quantity += quantity
#     else:
#         cart_item.quantity = quantity

#     cart_item.save()
#     return Response({"msg": "Added successfully"}, status=status.HTTP_201_CREATED)


# @api_view(['PUT'])
# @permission_classes([IsAuthenticated])
# def cart_update(request, pk):
#     cart_item = get_object_or_404(CartItem, id=pk, user=request.user)
#     quantity = request.data.get('quantity')
#     if quantity is not None:
#         cart_item.quantity = int(quantity)
#         cart_item.save()
#     serializer = CartItemSerializer(cart_item)
#     return Response(serializer.data, status=status.HTTP_200_OK)


# @api_view(['DELETE'])
# @permission_classes([IsAuthenticated])
# def cart_remove(request, pk):
#     cart_item = get_object_or_404(CartItem, id=pk, user=request.user)
#     cart_item.delete()
#     return Response({"message": "Deleted successfully"}, status=status.HTTP_200_OK)





#--------------------------------Now class based views---------------------------#



class RegisterUserView(APIView):
    permission_classes=[AllowAny]

    def post(self,request,*args,**kwargs):
        username = request.data.get('username')
        password = request.data.get('password')
        if not username or not password:
            return Response({"error":"Please provide username and password"},status=status.HTTP_400_BAD_REQUEST)
        if User.objects.filter(username=username).exists():
            return Response({"error":"user already exists"},status=status.HTTP_400_BAD_REQUEST)
        user=User.objects.create_user(username=username,password=password)

        # generate jwt tokens
        refresh = RefreshToken.for_user(user)
        access = refresh.access_token

        return Response({"msg":"User Created Successfully","access":str(access),"refresh":str(refresh)},status=status.HTTP_200_OK)




# One device at a time check as well as login

class CustomTokenObtainPairView(TokenObtainPairView):
    permission_classes=[AllowAny]
    def post(self, request, *args, **kwargs):
        response = super().post(request, *args, **kwargs)
        
        # Proceed if data authentication successful
        if response.status_code == 200:
            username = request.data.get('username')
            user = User.objects.get(username=username)
            refresh_token = response.data.get('refresh')

            # Check if user already has an active session
            existing_session = UserSession.objects.filter(user=user).first()
            if existing_session:
                # Blacklist the old refresh token
                try:
                    old_token = RefreshToken(existing_session.refresh_token)
                    old_token.blacklist()
                except Exception:
                    pass
                existing_session.delete()

            # Save new refresh token
            UserSession.objects.create(user=user, refresh_token=refresh_token)

        return response






class ProductListCreateView(generics.ListCreateAPIView):

    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    def perform_create(self, serializer):
        # Example: if you had created_by field, you can do:
        # serializer.save(created_by=self.request.user)
        serializer.save()


class ProductRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):

    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    # Optional: restrict updates/deletes to owners/admins by overriding:
    def perform_update(self, serializer):
        # If you had created_by on Product and wanted to restrict:
        # if self.request.user != self.get_object().created_by:
        #     raise PermissionDenied("You cannot edit someone else's product.")
        serializer.save()

    def perform_destroy(self, instance):
        # same idea for delete ownership check if needed
        instance.delete()



class CartView(generics.GenericAPIView):
    permission_classes=[IsAuthenticated]
    serializer_class = CartItemSerializer

    def get_queryset(self):
        return CartItem.objects.filter(user=self.request.user)


    def get(self,request,*agrs,**kwargs):
        items = self.get_queryset()
        serializer=self.get_serializer(items,many=True)
        total = sum(item.quantity*item.product.price for item in items)
        return Response({"item":serializer.data,"total":total},status=status.HTTP_200_OK)
    

    def post(self,request,*args,**kwargs):
        product_id = request.data.get('product_id')

        # try catch for quantity
        try:
            quantity = int(request.data.get('quantity',1))
        except (TypeError,ValueError):
            return Response({"error":"quantity must be integer"},status=status.HTTP_400_BAD_REQUEST)
        
        product = get_object_or_404(Product,id=product_id)

        cart_item,created = CartItem.objects.get_or_create(
            user=request.user,product=product,defaults={"quantity":quantity}
        )
        if not created:
            cart_item.quantity += quantity 
            cart_item.save()
        
        serializer=self.get_serializer(cart_item)

        return Response(serializer.data,status=status.HTTP_201_CREATED)

    def put(self,request,pk=None,*args,**kwargs):
        cart_item = get_object_or_404(self.get_queryset(),id=pk)
        quantity = request.data.get('quantity')
        if quantity is not None:
            cart_item.quantity= int(quantity)
            cart_item.save()
        serializer = self.get_serializer(cart_item)
        return Response(serializer.data,status=status.HTTP_200_OK)



    def delete(self,request,pk=None,*args,**kwargs):
        cart_item = get_object_or_404(self.get_queryset(),id=pk)
        cart_item.delete()
        return Response({"msg":f"item with {pk} is deleted successfully"},status=status.HTTP_200_OK)
    


    
    


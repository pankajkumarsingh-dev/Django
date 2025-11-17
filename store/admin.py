from django.contrib import admin
from .models import Product,CartItem

# Register your models here this is basic way

# admin.site.register(Product)
# admin.site.register(CartItem)

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display=['id','name','price','description']
    search_fields=['name','description']
    list_filter=['price']
    ordering=['id']

@admin.register(CartItem)
class CartItemAdmin(admin.ModelAdmin):
    list_display=['id','user','product_id','quantity']
    search_fields=['user__username','product___name']  #here the doulbe underscore is used to traverse the relationship to find values as product,user are foreign key to cartitem, this is orm method
    list_filter=['user']
    ordering=['id']


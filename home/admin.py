from django.contrib import admin
from .models import Category, Product, Cart, CartItem, Order, OrderItem

class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'description')
    search_fields = ('name',)

class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'stock', 'category')
    list_filter = ('category',)
    search_fields = ('name', 'description')
    # list_editable = ('price', 'stock')

class CartAdmin(admin.ModelAdmin):
    list_display = ('user', 'created_at')
    search_fields = ('user__username',)

class CartItemAdmin(admin.ModelAdmin):
    list_display = ('cart', 'product', 'quantity')
    list_filter = ('cart', 'product')
    search_fields = ('cart__user__username', 'product__name')

class OrderAdmin(admin.ModelAdmin):
    list_display = ('user', 'created_at', 'total_price','status')
    search_fields = ('user__username',)

class OrderItemAdmin(admin.ModelAdmin):
    list_display = ('order', 'product', 'quantity')
    list_filter = ('order', 'product')
    search_fields = ('order__user__username', 'product__name')

admin.site.register(Category, CategoryAdmin)
admin.site.register(Product, ProductAdmin)
admin.site.register(Cart, CartAdmin)
admin.site.register(CartItem, CartItemAdmin)
admin.site.register(Order, OrderAdmin)
admin.site.register(OrderItem, OrderItemAdmin)

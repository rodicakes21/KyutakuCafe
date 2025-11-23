from django.contrib import admin
from .models import Product, Order, CheckoutItem

# Register Product
@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'price')

# Register Order
@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'customer_name', 'user', 'created_at', 'total_price')
    readonly_fields = ('created_at',)

# Register CheckoutItem
@admin.register(CheckoutItem)
class CheckoutItemAdmin(admin.ModelAdmin):
    list_display = ('order', 'product', 'quantity', 'total_price')

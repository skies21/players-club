from django.contrib import admin
from .models import Product, Order, CartItem


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'is_available')
    list_filter = ('is_available',)
    search_fields = ('name', 'description')

admin.site.register(CartItem)
admin.site.register(Order)
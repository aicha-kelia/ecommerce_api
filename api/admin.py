
from django.contrib import admin
from .models import Customer, Product, Order, OrderItem, Review


@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'email', 'phone', 'created_at']
    search_fields = ['name', 'email']


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'price', 'category', 'stock', 'is_low_stock']
    list_filter = ['category']
    search_fields = ['name']


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 1


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['id', 'customer', 'status', 'total_amount', 'order_date']
    list_filter = ['status', 'order_date']
    inlines = [OrderItemInline]


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ['id', 'product', 'customer', 'rating', 'created_at']
    list_filter = ['rating']
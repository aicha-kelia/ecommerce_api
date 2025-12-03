from rest_framework import serializers
from .models import Customer, Product, Order, OrderItem, Review


class CustomerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customer
        fields = ['id', 'name', 'email', 'phone', 'address', 'created_at']
        read_only_fields = ['id', 'created_at']


class ReviewSerializer(serializers.ModelSerializer):
    customer_name = serializers.CharField(source='customer.name', read_only=True)

    class Meta:
        model = Review
        fields = ['id', 'product', 'customer', 'customer_name', 'rating', 'comment', 'created_at']
        read_only_fields = ['id', 'created_at']


class ProductSerializer(serializers.ModelSerializer):
    average_rating = serializers.FloatField(read_only=True)
    is_low_stock = serializers.BooleanField(read_only=True)
    reviews = ReviewSerializer(many=True, read_only=True)

    class Meta:
        model = Product
        fields = ['id', 'name', 'description', 'price', 'category', 'stock', 
                  'average_rating', 'is_low_stock', 'reviews', 'created_at', 'updated_at']
        read_only_fields = ['id', 'created_at', 'updated_at']


class ProductListSerializer(serializers.ModelSerializer):
    average_rating = serializers.FloatField(read_only=True)
    is_low_stock = serializers.BooleanField(read_only=True)

    class Meta:
        model = Product
        fields = ['id', 'name', 'price', 'category', 'stock', 'average_rating', 'is_low_stock']


class OrderItemSerializer(serializers.ModelSerializer):
    product_name = serializers.CharField(source='product.name', read_only=True)
    subtotal = serializers.DecimalField(max_digits=10, decimal_places=2, read_only=True)

    class Meta:
        model = OrderItem
        fields = ['id', 'product', 'product_name', 'quantity', 'price', 'subtotal']
        read_only_fields = ['id', 'price', 'subtotal']


class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True, read_only=True)
    customer_name = serializers.CharField(source='customer.name', read_only=True)
    total_amount = serializers.DecimalField(max_digits=10, decimal_places=2, read_only=True)

    class Meta:
        model = Order
        fields = ['id', 'customer', 'customer_name', 'order_date', 'status', 
                  'total_amount', 'items', 'updated_at']
        read_only_fields = ['id', 'order_date', 'updated_at']


class OrderCreateSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True)

    class Meta:
        model = Order
        fields = ['id', 'customer', 'items']

    def create(self, validated_data):
        from django.db import transaction
        
        items_data = validated_data.pop('items')
        
        with transaction.atomic():
            order = Order.objects.create(**validated_data)
            
            for item_data in items_data:
                product = item_data.get('product')
                quantity = item_data.get('quantity', 1)
                
                # Validate stock
                if product.stock < quantity:
                    raise serializers.ValidationError(
                        f"Not enough stock for {product.name}. Available: {product.stock}"
                    )
                
                # Create order item with price from product
                OrderItem.objects.create(
                    order=order,
                    product=product,
                    quantity=quantity,
                    price=product.price
                )
                
                # Deduct stock
                product.stock -= quantity
                product.save(update_fields=['stock'])
        
        return order
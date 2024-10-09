# serializers.py
from rest_framework import serializers
from .models import Product , Customer ,Order ,OrderItem
from django.contrib.auth.hashers import make_password 
from django.contrib.auth.models import User


class CustomerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customer
        fields = ['first_name', 'last_name', 'email', 'phone', 'birth_date', 'membership', 'password']
        extra_kwargs = {'password': {'write_only': True}}  # Ensure password is write-only
    
    def create(self, validated_data):
        return super().create(validated_data)

class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)

# Serializer for Product
class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'



# Serializer for OrderItem
class OrderItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderItem
        fields = ['id', 'order', 'product', 'quantity', 'unit_price']

# Serializer for Order
class OrderSerializer(serializers.ModelSerializer):
    # Include related OrderItems in the Order serialization
    items = OrderItemSerializer(source='orderitem_set', many=True, read_only=True)

    class Meta:
        model = Order
        fields = ['id', 'placed_at', 'payment_status', 'customer', 'items']

from rest_framework import serializers
from .models import Cart, CartItem, Order
from tours.serializers import TourSerializer

class CartItemSerializer(serializers.ModelSerializer):
    tour = TourSerializer()

    class Meta:
        model = CartItem
        fields = '__all__'

class CartSerializer(serializers.ModelSerializer):
    cart_items = CartItemSerializer(many=True, read_only=True)

    class Meta:
        model = Cart
        fields = '__all__'

class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = '__all__'
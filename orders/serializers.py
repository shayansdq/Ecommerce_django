from rest_framework import serializers

from orders.models import CartItem, Cart
from products.models import Product


class CheckValidOrderItem(serializers.Serializer):
    name = serializers.CharField()
    price = serializers.IntegerField()
    count = serializers.IntegerField()

    def update(self, instance, validated_data):
        pass

    def create(self, validated_data):
        pass


class CartItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = CartItem
        fields = ('cart', 'count', 'product')


class CartSerializer(serializers.ModelSerializer):
    off_code_str = serializers.ReadOnlyField()

    class Meta:
        model = Cart
        fields = ('total_price', 'final_price', 'off_code_str')


class LoadCartItem(serializers.ModelSerializer):
    name = serializers.ReadOnlyField(source='product.name')
    price = serializers.ReadOnlyField()

    class Meta:
        model = CartItem
        fields = ('name', 'price', 'count')

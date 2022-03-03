from rest_framework import serializers

from orders.models import CartItem


class CheckValidOrderItem(serializers.Serializer):
    name = serializers.CharField()
    price = serializers.IntegerField()
    count = serializers.IntegerField()

    def update(self, instance, validated_data):
        return instance

    def create(self, validated_data: dict):
        return Car.objects.create(**validated_data)

class CartItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = CartItem
        fields = ('name', 'count', 'price')

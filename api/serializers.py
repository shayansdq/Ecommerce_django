from rest_framework import serializers
from products.models import *
from comments.models import *
from customers.models import *
from orders.models import *


class ProductsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'

#
# class ServicesSerializer(serializers.ModelSerializer):
#     list_of_times = serializers.ReadOnlyField()
#
#     class Meta:
#         model = Service
#         fields = '__all__'
#
#
# class AgentsSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Agent
#         fields = '__all__'
#
#
# class BookingsSerializer(serializers.ModelSerializer):
#     agent_name = serializers.CharField(source='agent.name')
#
#     class Meta:
#         model = Booking
#         fields = '__all__'

from rest_framework import serializers

from customers.models import Address


class AddressSerializer(serializers.ModelSerializer):
    str = serializers.ReadOnlyField()

    class Meta:
        model = Address
        fields = ('id','state', 'city', 'zip_code', 'extra_detail', 'str')

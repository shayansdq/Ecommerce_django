from rest_framework import serializers

from customers.models import Address


class AddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = Address
        fields = ('state', 'city', 'zip_code', 'extra_detail')

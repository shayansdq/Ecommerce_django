from rest_framework import generics
from rest_framework.permissions import IsAuthenticated

from .models import Address, Customer
from customers.my_permissions import IsOwner
from customers.serializers import AddressSerializer


class AddressDetailApi(generics.RetrieveAPIView):
    permission_classes = [
        IsOwner,
    ]
    serializer_class = AddressSerializer
    queryset = Address.objects.all()


class AddressListApi(generics.ListAPIView):
    permission_classes = [
        IsAuthenticated,
    ]
    serializer_class = AddressSerializer
    queryset = Address.objects.all()

    def get_queryset(self):
        user = self.request.user
        this_customer = Customer.objects.get(user=user)
        addresses = Address.objects.filter(customer=this_customer)
        return addresses

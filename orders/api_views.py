from rest_framework import generics
from rest_framework.authentication import BasicAuthentication
from rest_framework.permissions import IsAuthenticated

from orders.models import Cart, CartItem
from orders.serializers import CartSerializer, LoadCartItem


class CartDetailApi(generics.ListAPIView):
    permission_classes = [
        IsAuthenticated,
    ]
    serializer_class = CartSerializer
    queryset = Cart.objects.all()

    def get_queryset(self):
        this_customer = self.request.user.customer
        return Cart.objects.filter(open=True, customer=this_customer)


class LoadCartItemsFromCart(generics.ListCreateAPIView):
    permission_classes = [
        IsAuthenticated
    ]
    authentication_classes = [
        BasicAuthentication
    ]


class LoadCartItemApi(generics.ListAPIView):
    permission_classes = [
        IsAuthenticated,
    ]
    serializer_class = LoadCartItem
    queryset = CartItem.objects.all()

    def get_queryset(self):
        this_customer = self.request.user.customer
        this_cart = Cart.objects.get(open=True, customer=this_customer)
        return this_cart.items.all()

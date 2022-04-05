from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import messages
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect
from django.views import View
# Create your views here.
from django.views.generic import CreateView, TemplateView
from rest_framework import generics
from rest_framework.authentication import BasicAuthentication
from rest_framework.permissions import IsAuthenticated

from customers.models import Customer, Address
from orders.forms import SubmitOrderForm
from orders.models import Cart, OffCode, CartItem
from orders.serializers import CheckValidOrderItem, CartItemSerializer, CartSerializer, LoadCartItem
from products.models import Product
import json


class CreateOrderView(LoginRequiredMixin, CreateView):

    def post(self, request, *args, **kwargs):
        CartItem.remove_loaded_items_key(request)
        CartItem.create_cart_item(request, CheckValidOrderItem, CartItemSerializer)
        return redirect('orders:cart_detail')


class ShoppingCartView(LoginRequiredMixin, TemplateView):
    template_name = 'orders/shopping_cart.html'

    def get_context_data(self, **kwargs):
        context = super(ShoppingCartView, self).get_context_data()
        order = Cart.objects.get(open=True, customer=self.request.user.customer)
        order_items = order.items.all()
        context['cart'] = order
        context['order_items'] = order_items
        context['form'] = SubmitOrderForm
        return context


class CheckOutCart(LoginRequiredMixin, View):
    def post(self, request):
        data = request.POST
        off_code = data.get('offcode')
        customer = request.user.customer
        cart = Cart.objects.get(customer=customer, open=True)
        address_id = data.get('address')
        if address_id == 'Select your address':
            return JsonResponse({'msg': 'You have to select an address!'})
        else:
            address = Address.objects.get(id=int(address_id))
            cart.address = address
            cart.save()
        if off_code:
            if OffCode.objects.filter(code=off_code).exists():
                code = OffCode.objects.get(code=off_code)
                cart.off_code = code
                cart.save()
                return JsonResponse({'msg': f'Your code ok with {code.value}'})
            else:
                cart.off_code = None
                cart.save()
                return JsonResponse({'msg': f'Your code is not valid!'})
        else:
            cart.off_code = None
            cart.save()
            return JsonResponse({'msg': f'Your address is ok'})
        return HttpResponse('ok')


class SubmitOrder(LoginRequiredMixin, View):
    def get(self, request):
        customer = request.user.customer
        cart = Cart.objects.get(open=True, customer=customer)
        cart.open = False
        cart.save()
        messages.success(request, 'Your order was successfully sent', 'success_login')
        return redirect('products:home')



from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import messages
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect
from django.views import View
# Create your views here.
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated

from customers.models import Customer, Address
from orders.forms import SubmitOrderForm
from orders.models import Cart, OffCode, CartItem
from orders.serializers import CheckValidOrderItem, CartItemSerializer, CartSerializer, LoadCartItem
from products.models import Product
import json


class CreateOrderView(LoginRequiredMixin, View):
    def post(self, request, *args, **kwargs):
        # print('ok')
        # if not request.user:
        #     redirect('customers:register_login_view')
        this_customer = request.user.customer
        last_order = Cart.objects.get_or_create(open=True, customer=this_customer)
        order = last_order[0]
        # print(order)
        if not last_order[1]:
            for cart_item in order.items.all():
                cart_item.delete()
        for i in request.POST.keys():
            i = json.loads(i)
            # print(i)
            # print(i)
            info = CheckValidOrderItem(data=i, many=True)
            if info.is_valid():
                for order_item in info.validated_data:
                    product = Product.objects.get(name=order_item['name'].replace('-', ' '))
                    print('t',product.name)
                    # count = order_item['count']
                    del order_item['name']
                    del order_item['price']
                    order_item['product'] = product.id
                    order_item['cart'] = order.id
                    print('t',order_item['product'],order_item['cart'])
                    print('o',dict(order_item))
                    cart_item = CartItemSerializer(data=dict(order_item))
                    # print(cart_item['product'])
                    # print(cart_item)
                    print(cart_item.is_valid())
                    if True or cart_item.is_valid():
                        # print(cart_item)

                        cart_item.save()
                    print(cart_item.errors)
            order.save()
            # print(info.validated_data)
        # print(type(request.POST))
        return redirect('orders:cart_detail')


class ShoppingCartView(LoginRequiredMixin, View):
    form_class = SubmitOrderForm

    # def setup(self, request, *args, **kwargs):
    #     if not request.user:
    #         redirect('customers:register_login_view')
    #     self.user = request.user
    #     self.customer = Customer.objects.get(user=self.user)
    #     super().setup(request, *args, **kwargs)

    def get(self, request):
        order = Cart.objects.get(open=True, customer=request.user.customer)
        order_items = order.items.all()
        context = {
            'cart': order,
            'order_items': order_items,
            'form': self.form_class,
        }
        return render(request, 'orders/shopping_cart.html', context)


class CheckOutCart(View):
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
        cart = Cart.objects.get(open=True,customer=customer)
        cart.open = False
        cart.save()
        messages.success(request, 'Your order was successfully sent', 'success_login')
        return redirect('products:home')


class CartDetailApi(generics.ListAPIView):
    permission_classes = [
        IsAuthenticated,
    ]
    serializer_class = CartSerializer
    queryset = Cart.objects.all()

    def get_queryset(self):
        this_customer = self.request.user.customer
        return Cart.objects.filter(open=True, customer=this_customer)


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

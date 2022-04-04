import json
from unicodedata import category
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin, messages
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect
from django.contrib.auth import views as auth_views
# Create your views here.
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import FormView, DeleteView, CreateView, ListView
from rest_framework import generics
from rest_framework import permissions, authentication
from rest_framework.permissions import IsAuthenticated

from core.models import User
from customers.forms import ContactUsForm, CustomerLoginForm, CustomerRegisterForm, CustomerForm, AddressForm, \
    VerifyCodeForm
from django.utils.translation import gettext as _

from customers.models import Address, Customer, OtpCode, WishList
from customers.my_permissions import IsOwner, SuperUserCanSee
from customers.serializers import AddressSerializer
from orders.models import Cart, CartItem
from orders.serializers import CartItemSerializer, LoadCartItem
from products.models import Category, Product
import random

from utils import send_otp_code, send_register_email


class ContactUsView2(SuccessMessageMixin, FormView):
    template_name = 'customers/contact.html'
    form_class = ContactUsForm
    success_url = reverse_lazy('contact_view')

    def post(self, request, *args, **kwargs):
        """
        Handle POST requests: instantiate a form instance with the passed
        POST variables and then check if it's valid.
        """
        form = self.get_form()
        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)


class ContactUsView(View):
    form_class = ContactUsForm

    def get(self, request, *args, **kwargs):
        form = self.form_class
        context = {
            'form': form,
            'title': _('Contact us')
        }
        return render(request, 'customers/contact.html', context=context)


class LoginRegisterView(View):
    login_form_class = CustomerLoginForm
    register_form_class = CustomerRegisterForm
    template_name = 'customers/login_register.html'

    def get(self, request, *args, **kwargs):
        login_form = self.login_form_class
        register_form = self.register_form_class
        context = {
            'login_form': login_form,
            'register_form': register_form,
        }
        return render(request, self.template_name, context)

    # post method for register user
    def post(self, request):
        register_form = self.register_form_class(request.POST)
        login_form = self.login_form_class()
        if register_form.is_valid():
            random_code = random.randint(1000, 9999)
            cd = register_form.cleaned_data
            # send_otp_code(cd['phone'], random_code)
            OtpCode.objects.create(phone=cd['phone'], code=random_code)
            request.session['user_registration_info'] = {
                'phone': cd['phone'],
                'password': cd['password1'],
                'email': cd['email'],
                'gender': cd['gender']
            }
            # new_user = User.objects.create_user(phone=cd['phone'], password=cd['password1'], email=cd['email'])
            # Customer.objects.create(user=new_user, gender=int(cd['gender']))
            messages.success(request, 'We Sent You a Code', 'success_register')
            return redirect('customers:verify_code')
        context = {
            'login_form': login_form,
            'register_form': register_form,
        }
        # Handle Invalid form

        # print(register_form.errors)
        messages.error(request, 'Registered unsuccessfully !', 'unsuccess_register')
        return render(request, self.template_name, context)


class UserRegisterVerifyCodeView(View):
    form_class = VerifyCodeForm

    def get(self, request):
        form = self.form_class
        context = {
            'form': form,
        }
        return render(request, 'customers/verify_code.html', context)

    def post(self, request):
        user_session = request.session['user_registration_info']
        code_instance = OtpCode.objects.get(phone=user_session['phone'])
        form = self.form_class(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            if cd['code'] == code_instance.code:
                new_user: User = User.objects.create_user(phone=user_session['phone'],
                                                          password=user_session['password'],
                                                          email=user_session['email'])
                new_customer = Customer.objects.create(user=new_user, gender=int(user_session['gender']))
                code_instance.delete()
                send_register_email(new_customer, cd['code'])
                user = authenticate(request, phone=new_user.phone, password=user_session['password'])
                login(request, user)
                messages.success(request, 'You registered successfully', 'success_register')
                return redirect('products:home')
            else:
                messages.error(request, 'This code is wrong', 'unsuccess_register')
                return redirect('customers:verify_code')
        context = {
            'form': form
        }
        return redirect('customers:verify_code')


class LoginPostView(View):
    login_form_class = CustomerLoginForm
    register_form_class = CustomerLoginForm

    def post(self, request, *args, **kwargs):
        login_form = self.login_form_class(request.POST)
        if login_form.is_valid():
            cd = login_form.cleaned_data
            user = authenticate(request, phone=cd['phone'], password=cd['password'])
            if user:
                login(request, user)
                messages.success(request, f'Login Successfully,Welcome {user.phone}', 'success_login')
                customer = user.customer
                if Cart.objects.filter(open=True, customer=customer).exists():
                    this_cart = Cart.objects.get(open=True, customer=customer)
                    ser_data = LoadCartItem(instance=this_cart.items.all(), many=True).data
                    request.session['loaded_items'] = ser_data
                    print(request.session.keys())
                    print('s', ser_data)
                # request.session['loaded_items'] = 'asd'
                return redirect('products:home')
        messages.error(request, 'your username or password is wrong', 'unsuccess_login')
        return redirect('customers:register_login_view')


class UserLogoutView(LoginRequiredMixin, View):
    """user logout view"""

    def get(self, request):
        logout(request)
        messages.success(request, 'You successfully logged out', 'success_login')
        return redirect('customers:register_login_view')


class UserPasswordResetView(auth_views.PasswordResetView):
    template_name = 'customers/password_reset_form.html'
    success_url = reverse_lazy('customers:password_reset_done')
    email_template_name = 'customers/password_reset_email.html'


class UserPasswordResetDoneView(auth_views.PasswordResetDoneView):
    template_name = 'customers/password_reset_done.html'


class UserPasswordResetConfirmView(auth_views.PasswordResetConfirmView):
    template_name = 'customers/password_reset_confirm.html'
    success_url = reverse_lazy('customers:password_reset_complete')


class UserPasswordResetCompleteView(auth_views.PasswordResetCompleteView):
    template_name = 'customers/password_reset_complete.html'


class CustomerProfileView(LoginRequiredMixin, View):
    info_user_form_class = CustomerForm

    def get(self, request, *args, **kwargs):
        CartItem.remove_loaded_items_key(request)
        user = request.user
        customer = Customer.objects.get(user=user)
        carts = customer.ccarts.all()
        user_info = {
            'phone': user.phone,
            'first_name': user.first_name,
            'last_name': user.last_name,
            'email': user.email
        }
        form = self.info_user_form_class(initial=user_info)
        categories = Category.objects.all()
        context = {
            'form': form,
            'categories': categories,
            'customer': customer,
            'carts': carts,
        }
        return render(request, 'customers/profile.html', context)

    def post(self, request, *args, **kwargs):
        form = self.info_user_form_class(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            request.user.phone = cd['phone']
            request.user.first_name = cd['first_name']
            request.user.last_name = cd['last_name']
            request.user.email = cd['email']
            request.user.save()
            messages.success(request, 'Congrats, your profile successfully edited', 'success_login')
            return redirect('customers:profile')
        context = {
            'form': form
        }
        return render(request, 'customers/profile.html', context)


class AddressCustomerProfileView(View):
    form_class = AddressForm

    def setup(self, request, *args, **kwargs):
        self.customer = request.user.customer
        self.addresses = Address.objects.filter(customer=self.customer)
        super().setup(request, *args, **kwargs)

    def get(self, request):
        CartItem.remove_loaded_items_key(request)
        context = {
            'form': self.form_class,
            'addresses': self.addresses,
            'customer': self.customer,
        }
        return render(request, 'customers/addresses_profile.html', context)

    def post(self, request):
        form = self.form_class(request.POST)
        if form.is_valid():
            address = form.save(commit=False)
            address.customer = self.customer
            address.save()
            messages.success(request, 'Your address was successfully created', 'success_login')
            return redirect('customers:profile_address')
        else:
            context = {
                'form': self.form_class,
                'addresses': self.addresses,
                'customer': self.customer,
            }
            return render(request, 'customers/addresses_profile.html', context)


class DeleteAddressView(DeleteView):
    model = Address
    # template_name = 'customers/address_check_delete.html'
    success_url = reverse_lazy('customers:profile_address')


class WishListView(View):
    def setup(self, request, *args, **kwargs):
        self.data = request.POST
        self.customer: Customer = request.user.customer if request.user.is_authenticated else None
        super(WishListView, self).setup(request, *args, **kwargs)

    def get(self, request):
        wishlist = list(map(lambda x: x.product, list(self.customer.wishlist.all())))
        context = {
            'wishlist': wishlist,
            'customer': self.request.user.customer
        }
        return render(request, 'customers/wishlist_profile.html', context)

    def post(self, request):
        self.do = self.data.get('do')
        self.product = Product.objects.get(pk=self.data.get('product_id'))
        if not self.customer:
            return JsonResponse({'msg': 'You have to login first'})
        elif self.do == 'like':
            WishList.objects.create(product=self.product, customer=self.customer)
            return JsonResponse({'msg': 'Added to your list'})
        else:
            WishList.objects.get(product=self.product, customer=self.customer).delete()
            return JsonResponse({'msg': 'Removed from your list'})
        return JsonResponse({'msg': 'Added to your list'})
        #     WishList.objects.get(product=self.product, customer=self.customer)
        #     pass
        # else
        # print(, '-ss-', data.get('product_id'))


class CustomerOrdersList(ListView):
    template_name = 'customers/orders_list.html'
    context_object_name = 'orders'

    def get_context_data(self, *, object_list=None, **kwargs):
        self.req


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

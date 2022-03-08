from unicodedata import category
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin, messages
from django.shortcuts import render, redirect
from django.contrib.auth import views as auth_views
# Create your views here.
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import FormView
from rest_framework import generics
from rest_framework import permissions, authentication
from rest_framework.permissions import IsAuthenticated

from core.models import User
from customers.forms import ContactUsForm, CustomerLoginForm, CustomerRegisterForm, CustomerForm, AddressForm
from django.utils.translation import gettext as _

from customers.models import Address, Customer
from customers.my_permissions import IsOwner, SuperUserCanSee
from customers.serializers import AddressSerializer
from products.models import Category


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
            cd = register_form.cleaned_data

            new_user = User.objects.create_user(phone=cd['phone'], password=cd['password1'], email=cd['email'])
            Customer.objects.create(user=new_user, gender=int(cd['gender']))
            messages.success(request, 'Registered successfully!', 'success_register')
            return redirect('customers:register_login_view')
        context = {
            'login_form': login_form,
            'register_form': register_form,
        }
        # Handle Invalid form

        print(register_form.errors)
        messages.error(request, 'Registered unsuccessfully !', 'unsuccess_register')
        return render(request, self.template_name, context)


class LoginPostView(View):
    login_form_class = CustomerLoginForm
    register_form_class = CustomerLoginForm

    # def setup(self, request, *args, **kwargs):
    #     self.next = request.POST.get('next')
    #     print(self.next)
    #     return super().setup(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        login_form = self.login_form_class(request.POST)
        register_form = self.register_form_class
        if login_form.is_valid():
            cd = login_form.cleaned_data
            user = authenticate(request, phone=cd['phone'], password=cd['password'])
            if user:
                login(request, user)
                # if self.next:
                #     return redirect(self.next)
                messages.success(request, f'Login Successfully,Welcome {user.phone}', 'success_login')
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
        super().setup(request, *args, **kwargs)

    def get(self, request):
        addresses = Address.objects.filter(customer=self.customer)
        context = {
            'form': self.form_class,
            'addresses': addresses,
            'customer': self.customer,
        }
        return render(request, 'customers/addresses_profile.html', context)


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

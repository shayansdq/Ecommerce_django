from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin, messages
from django.shortcuts import render, redirect

# Create your views here.
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import FormView

from core.models import User
from customers.forms import ContactUsForm, CustomerLoginForm, CustomerRegisterForm
from django.utils.translation import gettext as _


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
            print(cd)
            User.objects.create_user(phone=cd['phone'], password=cd['password1'], email=cd['email'])
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

    def setup(self, request, *args, **kwargs):
        self.next = request.GET.get('next')
        return super().setup(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        login_form = self.login_form_class(request.POST)
        register_form = self.register_form_class
        if login_form.is_valid():
            cd = login_form.cleaned_data
            user = authenticate(request, phone=cd['phone'], password=cd['password'])
            if user:
                login(request, user)
                if self.next:
                    return redirect(self.next)
                messages.success(request, f'Login Successfully,Welcome {user.phone}', 'success_login')
                return redirect('products:products_list')
        messages.error(request, 'your username or password is wrong', 'unsuccess_login')
        return redirect('customers:register_login_view')


class UserLogoutView(LoginRequiredMixin, View):
    """user logout view"""
    def get(self, request):
        logout(request)
        messages.success(request, 'You successfully logged out', 'success_login')
        return redirect('products:products_list')

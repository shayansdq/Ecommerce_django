from django import forms
from django.core.exceptions import ValidationError

from core.models import User
from customers.constants.validators import check_phone
from customers.constants.values import GENDER_STATUS_FORM


class ContactUsForm(forms.Form):
    email = forms.EmailField(widget=forms.TextInput(attrs={'class': 'form-control',
                                                           'placeholder': 'Email'}))
    name = forms.CharField(max_length=20, widget=forms.TextInput(attrs={'class': 'form-control',
                                                                        'placeholder': 'Name'}))
    message = forms.CharField(widget=forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Message'}))


class CustomerLoginForm(forms.Form):
    phone = forms.CharField(max_length=100,
                            widget=forms.TextInput(attrs={'placeholder': 'Phone'}))
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'placeholder': 'Password', 'class': 'form-control'}))

    def clean_phone(self):
        phone = self.cleaned_data.get('phone')
        return check_phone(phone)


class CustomerRegisterForm(forms.Form):
    phone = forms.CharField(max_length=100,
                            widget=forms.TextInput(attrs={'placeholder': 'Phone'}))

    email = forms.EmailField(max_length=100,
                             widget=forms.TextInput(attrs={'placeholder': 'Email'}))
    password1 = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'Password', 'class': 'form-control'}))
    password2 = forms.CharField(widget=forms.PasswordInput(
        attrs={'placeholder': 'Confirm password', 'class': 'form-control'}))
    gender = forms.ChoiceField(widget=forms.Select(), choices=GENDER_STATUS_FORM
                               )

    def clean_email(self):
        email = self.cleaned_data['email']
        user = User.objects.filter(email=email).exists()
        if user:
            raise ValidationError('This email address is already exists!')
        return email

    def clean_phone(self):
        phone = self.cleaned_data.get('phone')
        user = User.objects.filter(phone=phone).exists()
        if user:
            raise ValidationError('This phone is already exists!')
        return check_phone(phone)

    def clean(self):
        cd = super().clean()
        p1 = cd.get('password1')
        p2 = cd.get('password2')
        if p1 and p2 and p1 != p2:
            raise ValidationError('Passwords is not match')

from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import gettext_lazy as _
from core.models import BaseModel


class Customer(User):
    """
        A class used to implement customers
    """
    # first_name = models.CharField(max_length=32, verbose_name='First Name')
    # last_name = models.CharField(max_length=32, verbose_name='Last Name')
    # email = models.EmailField(verbose_name='Email')
    phone_number = models.CharField(max_length=32, verbose_name='Phone Number')
    gender = models.IntegerField(choices=[
        (1, 'Male'),
        (2, 'Female'),
        (3, 'Other'),
    ],verbose_name='Gender')

    class Meta:
        verbose_name = 'Customer'
        verbose_name_plural = 'Customers'


class Address(BaseModel):
    """
        A class used to implement customers
    """
    state = models.CharField(max_length=50, verbose_name='State')
    city = models.CharField(max_length=50, verbose_name='City')
    zip_code = models.PositiveIntegerField(unique=True,verbose_name='Zip Code')
    extra_detail = models.TextField(verbose_name='Address detail')
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name='addresses',verbose_name='Customer')

    class Meta:
        index_together = ["city", "zip_code"]
        unique_together = ["city", "zip_code"]
        verbose_name = 'Address'
        verbose_name_plural = 'Addresses'

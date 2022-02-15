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
    ])


class Address(BaseModel):
    """
        A class used to implement customers
    """
    state = models.CharField(max_length=50)
    city = models.CharField(max_length=50)
    zip_code = models.PositiveIntegerField(max_length=10,verbose_name='Zip Code')
    extra_detail = models.TextField()
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name='addresses')

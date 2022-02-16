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
    phone_number = models.CharField(max_length=32, verbose_name=_('Phone Number'))
    gender = models.IntegerField(choices=[
        (1, _('Male')),
        (2, _('Female')),
        (3, _('Other')),
    ],verbose_name=_('Gender'))

    class Meta:
        verbose_name = _('Customer')
        verbose_name_plural = _('Customers')


class Address(BaseModel):
    """
        A class used to implement customers
    """
    state = models.CharField(max_length=50, verbose_name=_('State'))
    city = models.CharField(max_length=50, verbose_name=_('City'))
    zip_code = models.PositiveIntegerField(unique=True,verbose_name=_('Zip Code'))
    extra_detail = models.TextField(verbose_name=_('Address detail'))
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name='addresses',
                                 verbose_name=_('Customer'))

    class Meta:
        index_together = ["city", "zip_code"]
        unique_together = ["city", "zip_code"]
        verbose_name = _('Address')
        verbose_name_plural = _('Addresses')

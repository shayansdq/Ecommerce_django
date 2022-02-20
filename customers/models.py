from django.db import models
from core.models import User
from django.utils.translation import gettext_lazy as _
from core.models import BaseModel
from .constants.values import *


class Customer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, verbose_name=_('User'))
    gender = models.IntegerField(choices=GENDER_STATUS, verbose_name=_('Gender'))

    class Meta:
        verbose_name = _('Customer')
        verbose_name_plural = _('Customers')

    def __str__(self):
        return f"Customer: '{self.user.phone}', Gender"


class Address(BaseModel):
    """
        A class used to implement customers
    """
    state = models.CharField(max_length=50, verbose_name=_('State'))
    city = models.CharField(max_length=50, verbose_name=_('City'))
    zip_code = models.PositiveIntegerField(unique=True, verbose_name=_('Zip Code'))
    extra_detail = models.TextField(verbose_name=_('Address detail'))
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name='addresses',
                                 verbose_name=_('Customer'))

    class Meta:
        index_together = ["city", "zip_code"]
        unique_together = ["city", "zip_code"]
        verbose_name = _('Address')
        verbose_name_plural = _('Addresses')

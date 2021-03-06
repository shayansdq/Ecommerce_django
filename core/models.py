from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import UserManager, AbstractUser
from django.core.exceptions import ValidationError
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from core.constants.values import *
from core.manager import BaseManager


class BaseModel(models.Model):
    """
        This model mixin usable for logical delete and logical activate status datas.
    """
    created = models.DateTimeField(auto_now_add=True, editable=False, verbose_name=_('Created'))
    last_updated = models.DateTimeField(auto_now=True, editable=False, verbose_name=_('Last updated'))
    delete_timestamp = models.DateTimeField(null=True, blank=True, verbose_name=_('Deleted timestamp'))
    deleted_at = models.DateTimeField(
        null=True, blank=True,
        verbose_name=_("Deleted Datetime"),
        help_text=_("This is deleted datetime")
    )
    is_deleted = models.BooleanField(
        default=False,
        verbose_name=_("Deleted status"),
        help_text=_("This is deleted status")
    )
    is_active = models.BooleanField(
        default=True,
        verbose_name=_("Active status"),
        help_text=_("This is active status")
    )

    # custom manager for get active items
    objects = BaseManager()

    class Meta:
        abstract = True

    def deleter(self):
        self.deleted_at = timezone.now()
        self.is_deleted = True
        self.save()

    def deactivate(self):
        self.is_active = False
        self.save()

    def activate(self):
        self.is_active = True
        self.save()


class MyUserManager(UserManager):

    def create_superuser(self, username=None, email=None, password=None, **extra_fields):
        username = extra_fields['phone']
        return super().create_superuser(username, email, password, **extra_fields)

    def create_user(self, username=None, email=None, password=None, **extra_fields):
        username = extra_fields['phone']
        return super().create_user(username, email, password, **extra_fields)

    def _create_user(self, username, email, password, **extra_fields):
        username = extra_fields['phone']
        return super()._create_user(username, email, password, **extra_fields)


class User(AbstractUser):
    phone = models.CharField(max_length=13, unique=True,verbose_name=_('Phone Number'),
                             help_text=_('Phone number used as username'))
    USERNAME_FIELD = 'phone'
    objects = MyUserManager()

    class Meta:
        verbose_name = _('User')
        verbose_name_plural = _('Users')

    def __str__(self):
        return f"Phone: {self.phone}"


class BaseDiscount(BaseModel):
    """
        Implement base discount
    """
    value = models.PositiveIntegerField(null=False, verbose_name=_('Value'))
    type = models.IntegerField(choices=DISCOUNT_STATUS, null=False,
                               verbose_name=_('Type'))
    max_price = models.PositiveIntegerField(null=True, blank=True, verbose_name=_('Max price'))

    def profit_value(self, price: int):
        """
        Calculate and Return the profit of the discount
        :param price: int (item value)
        :return: profit
        """
        if self.type == 0:
            return min(self.value, price)
        else:  # percent
            raw_profit = int((self.value / 100) * price)
            return int(min(raw_profit, int(self.max_price))) if self.max_price else raw_profit

    class Meta:
        abstract = True

    # Override the clean method for validating value in percent types
    def clean(self):
        if self.type == 'percent' and not 0 <= self.value <= 100:
            raise ValidationError({'value': _('Your value number must be between 0 and 100')})
        if self.type == 'price' and self.max_price:
            raise ValidationError({'max_price': _('In price type Should not have max price')})

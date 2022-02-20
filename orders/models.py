from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from core.models import BaseModel, BaseDiscount
from django.db import models
from customers.models import Customer, Address
from products.models import Product, Category
from django.core.validators import MinValueValidator, MinLengthValidator
from django.utils.text import slugify


class Cart(BaseModel):
    """
        A class used to implement carts
    """
    total_price = models.PositiveIntegerField(default=0, verbose_name=_('Total Price'))
    final_price = models.PositiveIntegerField(default=0, verbose_name=_('Final Price'))
    off_code = models.ForeignKey('OffCode', on_delete=models.CASCADE, related_name='carts', null=True, blank=True,
                                 verbose_name=_('Off Code'))
    customer = models.ForeignKey(Customer, on_delete=models.RESTRICT, related_name='ccarts', verbose_name=_('Customer'))
    address = models.ForeignKey(to=Address, on_delete=models.RESTRICT, related_name='acarts',verbose_name=_('Address'))

    def total_worth(self):
        """ 
            calculate total price of cart
        :return: total price amount (int)
        """
        self.total_price = sum([item.product.final_price for item in self.items.all()])
        return self.total_price

    def final_worth(self):
        """
        calculate final price of cart e.g with considering discounts
        :return: final price (int)
        """
        total = self.total_worth()
        self.final_price = total - self.off_code.profit_value(total) if self.off_code else total
        return self.final_price

    class Meta:
        index_together = [('customer', 'created'),
                          ('off_code', 'customer')]
        verbose_name = _('Cart')
        verbose_name_plural = _('Carts')

    def __str__(self):
        return f"{self.customer.user.phone} - {self.final_price}"


class CartItem(BaseModel):
    """
        A class used to implement cart items
    """

    count = models.PositiveIntegerField(default=1, verbose_name=_('Count'))
    cart = models.ForeignKey('Cart', on_delete=models.CASCADE, related_name='items', verbose_name=_('Cart'))
    product = models.OneToOneField(Product, on_delete=models.CASCADE, verbose_name=_('Product'))

    @classmethod
    def filter_by_product(cls, product: Product):
        """
        Filter all of Cart Items by a product
        :param product: (object of a product record)
        :return: all cart items that have this product
        """
        return cls.objects.filter(product=product)

    @classmethod
    def filter_by_product_category(cls, category: Category):
        """
         Filter all of Cart Items that their product consist of this category
        :param category: (object of a category record)
        :return: all cart items that their product consist of this category
        """
        return cls.objects.filter(product__category=category)

    class Meta:
        verbose_name = _('Cart Item')
        verbose_name_plural = _('Cart Items')

    def __str__(self):
        return f'{self.count} of {self.product}'


class OffCode(BaseDiscount):
    """
        A class to implement off codes
    """
    valid_from = models.DateTimeField(verbose_name=_('Valid from date'), help_text=_('Start date allowed to use'),
                                      validators=[MinValueValidator(timezone.now(), _('Must be greater than now'))])
    valid_to = models.DateTimeField(verbose_name=_('Valid to date'), help_text=_('End date allowed to use'))
    code = models.CharField(max_length=10, verbose_name=_('off code'),
                            help_text=_('The code that the customer must enter to use the discount'),
                            validators=[MinLengthValidator(10, _('Your code lengths should have exactly 10 chars'))])

    class Meta:
        verbose_name = _('Off code')
        verbose_name_plural = _('Off codes')

    def __str__(self):
        return f"Off Code {self.value}"

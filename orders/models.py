import json

from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from core.models import BaseModel, BaseDiscount
from django.db import models
from customers.models import Customer, Address
# from orders.serializers import CheckValidOrderItem, CartItemSerializer
from products.models import Product, Category
from django.core.validators import MinValueValidator, MinLengthValidator, MaxLengthValidator
from django.utils.text import slugify

from django.apps import apps


class Cart(BaseModel):
    """
        A class used to implement carts
    """
    total_price = models.PositiveIntegerField(default=0, verbose_name=_('Total Price'), null=True, blank=True, )
    final_price = models.PositiveIntegerField(default=0, verbose_name=_('Final Price'), null=True, blank=True, )
    off_code = models.ForeignKey('OffCode', on_delete=models.CASCADE, related_name='carts', null=True, blank=True,
                                 verbose_name=_('Off Code'))
    customer = models.ForeignKey(Customer, on_delete=models.RESTRICT, related_name='ccarts', verbose_name=_('Customer'))
    address = models.ForeignKey(to=Address, on_delete=models.RESTRICT, related_name='acarts', verbose_name=_('Address'),
                                null=True, blank=True)
    open = models.BooleanField(default=True)

    def total_worth(self):
        """ 
            calculate total price of cart
        :return: total price amount (int)
        """
        self.total_price = sum([item.product.final_price * item.count for item in self.items.all()])
        return self.total_price

    def final_worth(self):
        """
        calculate final price of cart e.g with considering discounts
        :return: final price (int)
        """
        total = self.total_worth()
        self.final_price = total - self.off_code.profit_value(total) if self.off_code else total

    @property
    def off_code_str(self):
        return str(self.off_code)

    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
        self.total_worth()
        self.final_worth()
        super().save(force_insert, force_update, using, update_fields)

    @property
    def profit(self):
        return self.total_price - self.final_price

    class Meta:
        index_together = [('customer', 'created'),
                          ('off_code', 'customer')]
        ordering = ('-created',)
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
    product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name=_('Product'))

    @classmethod
    def filter_by_product(cls, product: Product):
        """
        Filter all of Cart Items by a product
        :param product: (object of a product record)
        :return: all cart items that have this product
        """
        return cls.objects.filter(product=product)

    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):

        super().save(force_insert, force_update, using, update_fields)
        self.cart.save()

    @staticmethod
    def create_cart_item(request, CheckValidOrderItem, CartItemSerializer):

        this_customer = request.user.customer
        last_order = Cart.objects.get_or_create(open=True, customer=this_customer)
        order = last_order[0]
        if not last_order[1]:
            for cart_item in order.items.all():
                cart_item.delete()
        for i in request.POST.keys():
            i = json.loads(i)
            info = eval('CheckValidOrderItem(data=i, many=True)')
            if info.is_valid():
                for order_item in info.validated_data:
                    product = Product.objects.get(name=order_item['name'].replace('-', ' '))
                    del order_item['name']
                    del order_item['price']
                    order_item['product'] = product.id
                    order_item['cart'] = order.id
                    cart_item = eval('CartItemSerializer(data=dict(order_item))')
                    if cart_item.is_valid():
                        cart_item.save()
            order.save()

    @staticmethod
    def remove_loaded_items_key(request):
        if 'loaded_items' in request.session:
            request.session.pop('loaded_items')

    @classmethod
    def filter_by_product_category(cls, category: Category):
        """
         Filter all of Cart Items that their product consist of this category
        :param category: (object of a category record)
        :return: all cart items that their product consist of this category
        """
        return cls.objects.filter(product__category=category)

    @property
    def price(self):
        return self.product.final_price * self.count

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
    code = models.CharField(max_length=15, verbose_name=_('off code'),
                            help_text=_('The code that the customer must enter to use the discount'),
                            validators=[MaxLengthValidator(15, _('Your code lengths should have lower than 15 chars'))])

    class Meta:
        verbose_name = _('Off code')
        verbose_name_plural = _('Off codes')

    def __str__(self):
        sign = ' Tomans' if self.type == 0 else '%'
        return f"{self.value}" + sign

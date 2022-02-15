from core.models import BaseModel, BaseDiscount
from django.db import models
from customers.models import Customer
from products.models import Product


class Cart(BaseModel):
    """
        A class used to implement carts
    """
    total_price = models.PositiveIntegerField(default=0, verbose_name='Total Price')
    final_price = models.PositiveIntegerField(default=0, verbose_name='Final Price')
    off_code = models.ForeignKey('OffCode', on_delete=models.CASCADE, related_name='carts', null=True, blank=True,
                                 verbose_name='Off Code')
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name='carts',verbose_name='Customer')

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


class CartItem(BaseModel):
    """
        A class used to implement cart items
    """

    count = models.PositiveIntegerField(default=1,verbose_name='Count')
    cart = models.ForeignKey('Cart', on_delete=models.CASCADE, related_name='items',verbose_name='Cart')
    product = models.OneToOneField(Product, on_delete=models.CASCADE,verbose_name='Product')

    def __str__(self):
        return f'{self.count} of {self.product}'


class OffCode(BaseDiscount):
    """
        A class to implement off codes
    """
    valid_from = models.DateTimeField(verbose_name='Valid from date',help_text='Start date allowed to use')
    valid_to = models.DateTimeField(verbose_name='Valid to date',help_text='End date allowed to use')
    code = models.CharField(max_length=50, verbose_name='off code',help_text='The code ')

    def __str__(self):
        return f"Off Code {self.value}"

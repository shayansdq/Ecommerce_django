from django.db import models
from core.models import BaseModel, BaseDiscount


class Product(BaseModel):
    """
        A class used to implement products
    """
    name = models.CharField(max_length=100, verbose_name='Name')
    price = models.PositiveIntegerField(default=0, verbose_name='Price')
    description = models.TextField()
    picture = models.FileField(verbose_name='product image', null=True, blank=True)
    inventory = models.PositiveIntegerField()
    slug = models.SlugField(max_length=30, help_text='a short label for product')
    brand = models.ForeignKey('Brand', on_delete=models.CASCADE)
    discount = models.ForeignKey('Discount', on_delete=models.CASCADE, blank=True, null=True)
    category = models.ForeignKey('Category', on_delete=models.CASCADE)

    class Meta:
        ordering = ['-created']

    @property
    def is_available(self):
        return self.inventory > 0

    @property
    def final_price(self):
        """
        calculate price with discounts
        :return:
        """
        return self.price - self.discount.profit_value(self.price) if self.discount else self.price

    def __str__(self):
        return f'{self.name}'


class Brand(BaseModel):
    """
        implement brands
    """
    name = models.CharField(max_length=50, verbose_name='Name')
    country = models.CharField(max_length=50, verbose_name='Country')

    def __str__(self):
        return self.name


class Category(BaseModel):
    """
        implement categories
    """
    name = models.CharField(max_length=100, verbose_name='Name')
    root = models.ForeignKey('self', on_delete=models.CASCADE, default=None, null=True, blank=True)
    discount = models.ForeignKey('Discount', on_delete=models.CASCADE, blank=True, null=True)

    class Meta:
        verbose_name_plural = "categories"

    def __str__(self):
        return self.name


class Discount(BaseDiscount):
    """
        Implement discounts
    """

    def __str__(self):
        return f'Discount {self.value}'

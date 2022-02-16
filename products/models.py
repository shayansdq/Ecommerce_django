from django.db import models
from django.db.models import Max
from django.utils.translation import gettext_lazy as _
from core.models import BaseModel, BaseDiscount


class Category(BaseModel):
    """
        implement categories
    """
    name = models.CharField(max_length=100, verbose_name='Name')
    root = models.ForeignKey('self', on_delete=models.CASCADE, default=None, null=True, blank=True)
    discount = models.ForeignKey('Discount', on_delete=models.CASCADE, blank=True, null=True)

    class Meta:
        verbose_name = _("category")
        verbose_name_plural = _("categories")

    def __str__(self):
        return _(f"{self.name} from {self.root.name}" if self.root else f"{self.name}")


class Product(BaseModel):
    """
        A class used to implement products
    """
    name = models.CharField(max_length=100, verbose_name='Name')
    price = models.PositiveIntegerField(default=0, verbose_name='Price')
    description = models.TextField(verbose_name='Des')
    image = models.FileField(verbose_name='Product image', null=True, blank=True)
    inventory = models.PositiveIntegerField(verbose_name='Inventory')
    slug = models.SlugField(max_length=30, help_text='a short label for product', verbose_name='Slug')
    brand = models.ForeignKey('Brand', on_delete=models.CASCADE, verbose_name='Brand')
    discount = models.ForeignKey('Discount', on_delete=models.CASCADE, blank=True, null=True, verbose_name='Discount')
    category = models.ForeignKey('Category', on_delete=models.CASCADE, verbose_name='Category')

    class Meta:
        ordering = ['-created']
        verbose_name = _("Product")
        verbose_name_plural = _("Products")

    @classmethod
    def filter_by_category(cls, category: Category):
        """
        Filter all Products by a Category
        :param category: (object of a product record)
        :return: all products that consist of this category
        """
        return cls.objects.filter(category=category)

    @classmethod
    def max_price(cls):
        """

        :return: all products that consist of this category
        """
        return cls.objects.get(price=cls.objects.aggregate(max_price=Max('price')).get('max_price'))

    @property
    def is_available(self):
        self.is_active = self.inventory > 0
        return self.is_active

    @property
    def final_price(self):
        """
        calculate price with discounts
        :return:
        """
        return self.price - self.discount.profit_value(self.price) if self.discount else self.price

    def __str__(self):
        return _(f'{self.name}')


class Brand(BaseModel):
    """
        implement brands
    """
    name = models.CharField(max_length=50, verbose_name=_('Name'))
    country = models.CharField(max_length=50, verbose_name=_('Country'))

    class Meta:
        ordering = ['name']
        verbose_name = _("Brand")
        verbose_name_plural = _("Brands")

    def __str__(self):
        return _(f"{self.name} from {self.country}")


class Discount(BaseDiscount):
    """
        Implement discounts
    """

    class Meta:
        ordering = ['-value']
        verbose_name = _("Discount")
        verbose_name_plural = _("Discounts")

    def __str__(self):
        return _(f'Discount value: {self.value}')

from django.db import models
from django.db.models import Max
from django.utils.translation import gettext_lazy as _
from core.models import BaseModel, BaseDiscount
from django.urls import reverse

from customers.models import Customer


class Category(BaseModel):
    """
        implement categories
    """
    name = models.CharField(max_length=100, verbose_name='Name')
    slug = models.SlugField(max_length=50, unique=True,
                            help_text=_('Unique value for product page URL, created from name.'))
    root = models.ForeignKey('self', on_delete=models.CASCADE, default=None, null=True, blank=True)
    description = models.TextField()
    meta_keywords = models.CharField("Meta Keywords", max_length=255,
                                     help_text=_('Comma-delimited set of SEO keywords for meta tag'))
    meta_description = models.CharField("Meta Description", max_length=255,
                                        help_text=_('Content for description meta tag'))

    class Meta:
        db_table = 'categories'
        ordering = ['-created']
        verbose_name = _("category")
        verbose_name_plural = _("categories")

    def __unicode__(self):
        return self.name

    def get_absolute_url(self):
        pass
        # return reverse('home:post_detail', args=(self.id, self.slug))

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
    slug = models.SlugField(max_length=30, verbose_name='Slug',
                            help_text='Unique value for product page URL, created from name.')
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

    def get_absolute_url(self):
        pass
        # return reverse('home:post_detail', args=(self.id, self.slug))

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


class Comment(BaseModel):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name='ccomments',
                                 verbose_name=_('Customer'))
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='pcomments',verbose_name=_('Product'))
    reply = models.ForeignKey('self', on_delete=models.CASCADE, related_name='rcomments', null=True, blank=True,
                              verbose_name=_('Reply'))
    is_reply = models.BooleanField(default=False,verbose_name=_('Is reply'),
                                   help_text=_('Selected if this comment is a reply message from another customer'))
    body = models.TextField(max_length=400,verbose_name=_('Body'))

    class Meta:
        ordering = ['-created']
        verbose_name = _("Comment")
        verbose_name_plural = _("Comments")

    def __str__(self):
        return _(f"{self.customer} - {self.body[:30]}")

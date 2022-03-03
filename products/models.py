from django.core.exceptions import ValidationError
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
    name = models.CharField(max_length=100, verbose_name='Name', unique=True)
    slug = models.SlugField(max_length=50, unique=True, blank=True,
                            help_text=_('Unique value for product page URL, created from name.'))
    image = models.FileField(verbose_name=_('Category image'), null=True, blank=True)
    root = models.ForeignKey('self', on_delete=models.CASCADE, default=None, null=True, blank=True,
                             related_name='child')
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

    @classmethod
    def popular_categories(cls, count):
        categories = cls.objects.all()
        list_popular_categories = list(categories)
        # for c in list(categories):
        #     print(c.product_set.all().count())
        list_popular_categories.sort(reverse=True, key=lambda x: x.product_set.all().count())
        return list_popular_categories[:count]

    def children_products(self):
        products = Product.objects.filter(category=self)
        products = list(products)
        if self.child.all():
            for child_category in list(self.child.all()):
                products.extend(list(Product.objects.filter(category=child_category)))
        return products


    def get_absolute_url(self):
        pass
        # return reverse('home:post_detail', args=(self.id, self.slug))

    def __str__(self):
        return f"{self.name} from {self.root.name}" if self.root else f"{self.name}"


class Product(BaseModel):
    """
        A class used to implement products
    """
    name = models.CharField(max_length=100, verbose_name=_('Name'), unique=True)
    price = models.PositiveIntegerField(default=0, verbose_name=_('Price'))
    final_price = models.PositiveIntegerField(null=True, blank=True, verbose_name=_('Final Price'))
    description = models.TextField(verbose_name='Des')
    image = models.FileField(verbose_name=_('Product image'), null=True, blank=True)
    inventory = models.PositiveIntegerField(verbose_name=_('Inventory'))
    slug = models.SlugField(max_length=30, verbose_name=_('Slug'),
                            help_text=_('Unique value for product page URL, created from name.'))
    brand = models.ForeignKey('Brand', on_delete=models.CASCADE, verbose_name=_('Brand'))
    discount = models.ForeignKey('Discount', on_delete=models.CASCADE, blank=True, null=True,
                                 verbose_name=_('Discount'))
    category = models.ForeignKey('Category', on_delete=models.CASCADE, verbose_name=_('Category'))

    class Meta:
        ordering = ['-created']
        verbose_name = _("Product")
        verbose_name_plural = _("Products")

    @classmethod
    def has_discount(cls):
        return cls.objects.filter(discount__value__in=range(0, 90))

    @classmethod
    def filter_by_category(cls, category: Category):
        """
        Filter all Products by a Category
        :param category: (object of a product record)
        :return: all products that consist of this category
        """
        return cls.objects.filter(category=category)

    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
        self.final_worth()
        super().save(force_insert, force_update, using, update_fields)

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

    @staticmethod
    def brand_of_products(products_lst: list):
        brands = set()
        for p in products_lst:
            brands.add(p.brand)
        return list(brands)


    def final_worth(self):
        """
        calculate price with discounts
        :return:
        """
        self.final_price = self.price - self.discount.profit_value(self.price) if self.discount else self.price

    @classmethod
    def most_discounted_products(cls, count: int):
        products = cls.objects.all()
        res_list = list(products)
        has_discount_products = list(filter(lambda x: x.discount and x.discount.type == 1, res_list))
        has_discount_products.sort(reverse=True, key=lambda x: x.discount.value)
        return has_discount_products[:count]

    def search_parent_categories(self):
        list_categories = [self.category]
        if self.category.root:
            list_categories.append(self.category.root)
            if self.category.root.root:
                list_categories.append(self.category.root.root)
                if self.category.root.root.root:
                    list_categories.append(self.category.root.root.root)
        return list_categories[::-1]

    def get_absolute_url(self):
        pass
        # return reverse('home:post_detail', args=(self.id, self.slug))

    def __str__(self):
        return f'{self.name}'


class Brand(BaseModel):
    """
        implement brands
    """
    name = models.CharField(max_length=50, verbose_name=_('Name'))
    country = models.CharField(max_length=50, verbose_name=_('Country'))
    image = models.FileField(verbose_name=_('Category image'), null=True, blank=True)

    class Meta:
        ordering = ['name']
        verbose_name = _("Brand")
        verbose_name_plural = _("Brands")

    def __str__(self):
        return f"{self.name} from {self.country}"


class Discount(BaseDiscount):
    """
        Implement discounts
    """

    class Meta:
        ordering = ['-value']
        verbose_name = _("Discount")
        verbose_name_plural = _("Discounts")

    def __str__(self):
        return f'Discount value: {self.value}'


class ProductImages(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='extra_images')
    image = models.FileField(verbose_name=_('Image'),
                             help_text=_('Extra image for product and show more detail'))

    # def __str__(self):
    #     for product_image in self.product.images
    #     return f""

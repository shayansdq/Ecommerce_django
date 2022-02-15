from django.db.models import Count
from django.utils import timezone

from orders.models import Cart, CartItem, OffCode
from customers.models import Customer
from products.models import Product, Brand, Discount, Category
from django.test import TestCase


class ProductTest(TestCase):
    def setUp(self) -> None:
        self.customer1 = Customer.objects.create_user('test1', 'test1@email.com', 'test1', gender=1,
                                                      phone_number='09224023292')
        # self.off_code1 = OffCode.objects.create(value=10000, type='PRI', code='abcd123465')
        self.cart1 = Cart.objects.create(customer=self.customer1)

        # brands
        self.brand1 = Brand.objects.create(name='LG', country='Japan')
        self.brand2 = Brand.objects.create(name='samsung', country='Korea')

        # categories
        self.category1 = Category.objects.create(name='Electrical')
        self.category2 = Category.objects.create(name='mobile', root=self.category1)

        # discounts
        self.discount1 = Discount.objects.create(value=2000, type='PR')
        self.discount2 = Discount.objects.create(value=35, type='PE')

        # products
        self.product1 = Product.objects.create(name='TV', price=100000, description='some text', inventory=5,
                                               brand=self.brand1,
                                               category=self.category1, discount=self.discount1, slug='some-text')
        self.product2 = Product.objects.create(name='J5', price=200, description='some text', inventory=10,
                                               brand=self.brand2,
                                               category=self.category2, slug='another-text')

        # cart items

        self.cart_item1 = CartItem.objects.create(cart=self.cart1, product=self.product1)
        self.cart_item2 = CartItem.objects.create(cart=self.cart1, product=self.product2)

    def test1_find_max_price_product(self):
        # self.assertEqual(Product.max_price(),Product.objects.all().values())
        max_price = max(Product.objects.all().values_list('price', flat=True))
        self.assertEqual(Product.max_price().price, max_price)
        print(Product.objects.annotate(Count('brand')))

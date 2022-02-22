from django.utils.text import slugify

from orders.models import Cart, CartItem, OffCode
from customers.models import Customer
from products.models import Product, Brand, Discount, Category
from django.test import TestCase


class CartTest(TestCase):
    def setUp(self) -> None:
        self.customer1 = Customer.objects.create_user('shayan', 'shayan@gmail.com', 'shayan', gender=1,
                                                      phone_number='09216791779')
        self.customer2 = Customer.objects.create_user('zahra', 'zahra@gmail.com', 'zahra', gender=2,
                                                      phone_number='09237658735')
        # self.off_code1 = OffCode.objects.create(value=10000, type='PRI', code='abcd123465')
        self.cart1 = Cart.objects.create(customer=self.customer1)
        self.cart2 = Cart.objects.create(customer=self.customer2)

        # brands
        self.brand1 = Brand.objects.create(name='LG', country='Japan')
        self.brand2 = Brand.objects.create(name='Samsung', country='Korea')
        self.brand3 = Brand.objects.create(name='Apple', country='USA')
        self.brand4 = Brand.objects.create(name='Lo real', country='Germany')
        self.brand5 = Brand.objects.create(name='Tom Ford', country='USA')

        # categories
        self.category1 = Category.objects.create(name='Electrical', description='asdas', slug=slugify('asdas'),
                                                 meta_keywords='asdas', meta_description='asda')
        self.category2 = Category.objects.create(name='Mobile', root=self.category1,description='asdas',
                                                 slug=slugify('asdas'),
                                                 meta_keywords='asdas', meta_description='asda')
        self.category3 = Category.objects.create(name='Laptop', root=self.category1,description='asdas',
                                                 slug=slugify('asdas'),
                                                 meta_keywords='asdas', meta_description='asda')
        self.category4 = Category.objects.create(name='Cosmetic',description='asdas', slug=slugify('asdas'),
                                                 meta_keywords='asdas', meta_description='asda')
        self.category5 = Category.objects.create(name='Face', root=self.category4,description='asdas',
                                                 slug=slugify('asdas'),
                                                 meta_keywords='asdas', meta_description='asda')
        self.category6 = Category.objects.create(name='Foot', root=self.category4,description='asdas',
                                                 slug=slugify('asdas'),
                                                 meta_keywords='asdas', meta_description='asda')

        # discounts
        self.discount1 = Discount.objects.create(value=2000, type='PR')
        self.discount2 = Discount.objects.create(value=35, type='PE')

        # products
        self.product1 = Product.objects.create(name='good mobile', price=100000, description='some text', inventory=5,
                                               brand=self.brand1,
                                               category=self.category1, discount=self.discount1, slug=slugify('asdas'))
        self.product2 = Product.objects.create(name='nice laptop', price=200000, description='some text', inventory=10,
                                               brand=self.brand2,
                                               category=self.category2, slug=slugify('asdas'))

        # cart items

        self.cart_item1 = CartItem.objects.create(cart=self.cart1, product=self.product1)
        self.cart_item2 = CartItem.objects.create(cart=self.cart1, product=self.product2)

    def test1_total_worth_success(self):
        print(self.cart1.total_worth())

    def test2_final_worth_success(self):
        print(self.cart1.final_worth())


from django.test import TestCase
from django.utils.text import slugify

from core.models import User
from customers.models import Customer, Address

# Create your tests here.
from orders.models import Cart, CartItem
from products.models import Brand, Category, Discount, Product


class TestCommentModel(TestCase):
    def setUp(self) -> None:
        self.user1 = User.objects.create_user(phone='0921791779', password='123123')
        self.customer1 = Customer.objects.create(user=self.user1, gender=1)
        self.add1 = Address.objects.create(state='asd',city='assd',zip_code=1231,extra_detail='asda',
                                           customer=self.customer1)
        self.add2 = Address.objects.create(state='123',city='dfgd',zip_code=234,extra_detail='aska',
                                           customer=self.customer1)
        self.cart1 = Cart.objects.create(customer=self.customer1,address=self.add1)
        self.cart2 = Cart.objects.create(customer=self.customer1,address=self.add2)

        # brands
        self.brand1 = Brand.objects.create(name='LG', country='Japan')
        self.brand2 = Brand.objects.create(name='Samsung', country='Korea')
        self.brand3 = Brand.objects.create(name='Apple', country='USA')
        self.brand4 = Brand.objects.create(name='Lo real', country='Germany')
        self.brand5 = Brand.objects.create(name='Tom Ford', country='USA')

        # categories
        self.category1 = Category.objects.create(name='Electrical', description='asdas', slug=slugify('afeesdas'),
                                                 meta_keywords='asdas', meta_description='asda')
        self.category2 = Category.objects.create(name='Mobile', root=self.category1, description='asdas',
                                                 slug=slugify('asdass'),
                                                 meta_keywords='asdas', meta_description='asda')
        self.category3 = Category.objects.create(name='Laptop', root=self.category1, description='asdas',
                                                 slug=slugify('asdasdc'),
                                                 meta_keywords='asdas', meta_description='asda')
        self.category4 = Category.objects.create(name='Cosmetic', description='asdas', slug=slugify('ferasdas'),
                                                 meta_keywords='asdas', meta_description='asda')
        self.category5 = Category.objects.create(name='Face', root=self.category4, description='asdas',
                                                 slug=slugify('asfredas'),
                                                 meta_keywords='asdas', meta_description='asda')
        self.category6 = Category.objects.create(name='Foot', root=self.category4, description='asdas',
                                                 slug=slugify('asdfrefas'),
                                                 meta_keywords='asdas', meta_description='asda')

        # discounts
        self.discount1 = Discount.objects.create(value=2000, type=0)
        self.discount2 = Discount.objects.create(value=35, type=1)

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

    def test1_comment(self):
        print(self.user1)
        print(self.customer1)


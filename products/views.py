import requests
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404
from django.views import View
from rest_framework.response import Response
from rest_framework import generics
from django.views.generic import DetailView, ListView

from comments.forms import CommentCreateForm, CommentReplyForm
from customers.models import WishList
from orders.models import CartItem, Cart
from orders.serializers import LoadCartItem
from .models import Product, Category, Brand
from .serializers import ProductSerializer


class ProductListView(ListView):
    model = Product
    context_object_name = 'products'
    paginate_by = 3
    template_name = 'products/index.html'

    def get_context_data(self, **kwargs):
        context = super(ProductListView, self).get_context_data(**kwargs)
        list_products = Product.objects.all()
        banner_products = Product.most_discounted_products(3)
        active_carousel = banner_products.pop(0)
        another_carousels = banner_products
        categories = Category.popular_categories(3)
        featured_products = Product.most_discounted_products(3)
        context['categories_3'] = categories
        context['products'] = featured_products
        context['another_carousels'] = another_carousels
        context['active_carousel'] = active_carousel
        return context


class ProductDetailView(DetailView):
    model = Product
    template_name = 'products/product_detail.html'

    def dispatch(self, request, *args, **kwargs):
        CartItem.remove_loaded_items_key(request)
        request.session['product_cm'] = self.kwargs.get('pk')
        # print(self.kwargs.get('pk'))
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(ProductDetailView, self).get_context_data(**kwargs)
        this_product: Product = self.object
        parent_categories = this_product.search_parent_categories()
        this_category = parent_categories.pop()
        another_categories = parent_categories
        related_products = Product.objects.filter(category=this_product.category)
        related_products = set(list(related_products)) - {this_product}
        slider_one_images = this_product.extra_images.all()[:3]
        slider_two_images = this_product.extra_images.all()[3:6]
        cm_form = CommentCreateForm()
        reply_cm_form = CommentReplyForm()
        print(str(self.request.user))
        is_like = WishList.objects.filter(customer=self.request.user.customer, product=this_product).exists() if \
            self.request.user.is_authenticated else None
        print(is_like)
        comments = this_product.pcomments.filter(is_reply=False)
        context['cm_form'] = cm_form
        context['reply_cm_form'] = reply_cm_form
        context['comments'] = comments
        context['this_category'] = this_category
        context['another_categories'] = another_categories
        context['slider_one_images'] = slider_one_images
        context['slider_two_images'] = slider_two_images
        context['related_products'] = related_products
        context['is_like'] = is_like
        return context


class ProductByCategoryListView(ListView):
    model = Product
    context_object_name = 'products'
    template_name = 'products/products_by_category.html'
    paginate_by = 3

    def dispatch(self, request, *args, **kwargs):
        CartItem.remove_loaded_items_key(request)
        return super().dispatch(request, *args, **kwargs)

    def get_queryset(self):
        self.category = Category.objects.get(pk=self.kwargs['pk'])
        return self.category.children_products()

    def get_context_data(self, **kwargs):
        context = super(ProductByCategoryListView, self).get_context_data(**kwargs)
        all_products = self.category.children_products()
        paginator = Paginator(self.get_queryset(), self.paginate_by)
        page = self.request.GET.get('page')
        this_brands = Product.brand_of_products(all_products)
        try:
            file_exams = paginator.page(page)
        except PageNotAnInteger:
            file_exams = paginator.page(1)
        except EmptyPage:
            file_exams = paginator.page(paginator.num_pages)
        context['list_exams'] = file_exams
        context['brands'] = this_brands
        return context

import requests
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.http import JsonResponse
from django.shortcuts import render
from django.views import View
from rest_framework.response import Response
from rest_framework import generics
from django.views.generic import DetailView, ListView
from .forms import PostSearchForm
from .models import Product, Category
from .serializers import ProductSerializer


class ProductListView(ListView):
    model = Product
    context_object_name = 'products'
    paginate_by = 3
    template_name = 'products/index.html'

    def get_context_data(self, **kwargs):
        context = super(ProductListView, self).get_context_data(**kwargs)
        list_products = Product.objects.all()
        paginator = Paginator(list_products, self.paginate_by)
        page = self.request.GET.get('page')
        try:
            file_exams = paginator.page(page)
        except PageNotAnInteger:
            file_exams = paginator.page(1)
        except EmptyPage:
            file_exams = paginator.page(paginator.num_pages)

        context['list_exams'] = file_exams
        return context


class ProductDetailView(DetailView):
    model = Product
    template_name = 'products/product_detail.html'

    def get_context_data(self, **kwargs):
        context = super(ProductDetailView, self).get_context_data(**kwargs)
        this_product = self.object
        related_products = Product.objects.filter(category=this_product.category)
        related_products = set(list(related_products)) - {this_product}
        slider_one_images = this_product.extra_images.all()[:3]
        slider_two_images = this_product.extra_images.all()[3:6]
        context['slider_one_images'] = slider_one_images
        context['slider_two_images'] = slider_two_images
        context['related_products'] = related_products
        return context


class ProductByCategoryListView(ListView):
    model = Product
    context_object_name = 'products'
    template_name = 'products/products_by_category.html'
    paginate_by = 2

    def get_context_data(self, **kwargs):
        context = super(ProductByCategoryListView, self).get_context_data(**kwargs)
        category = Category.objects.get(pk=self.kwargs['pk'])
        products = Product.objects.filter(category=category)
        products = list(products)
        if category.child.all():
            for child_category in list(category.child.all()):
                products.extend(list(Product.objects.filter(category=child_category)))
        context['products'] = products
        return context



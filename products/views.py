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
    # def get(self, request, *args, **kwargs):
    #     products = Product.objects.all()
    #     context = {
    #         'products': products,
    #     }
    #     return render(request, 'products/index.html', context)


class ProductDetailView(DetailView):
    model = Product
    template_name = 'products/product_detail.html'

    def get_context_data(self, **kwargs):
        context = super(ProductDetailView, self).get_context_data(**kwargs)
        categories = Category.objects.all()
        this_product = self.object
        related_products = Product.objects.filter(category=this_product.category)
        related_products = set(list(related_products)) - set([this_product])
        slider_one_images = this_product.extra_images.all()[:3]
        slider_two_images = this_product.extra_images.all()[3:6]

        context['categories'] = categories
        context['slider_one_images'] = slider_one_images
        context['slider_two_images'] = slider_two_images
        context['related_products'] = slider_two_images

        return context


# class ProductByCategoryListView(View):
#     def get(self, request, *args, **kwargs):
#         pass

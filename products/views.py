from django.http import JsonResponse
from django.shortcuts import render
from django.views import View
from rest_framework.response import Response
from rest_framework import generics
from .models import Product
from .serializers import ProductSerializer


# Create your views here.
#
# def product_list_api(request):
#     """
#     POST: create Product
#     GET: List Products
#     :param request:
#     """
#
#     if request.method == 'GET':
#         product_serializer = ProductSerializer(Product.objects.all(), many=True)
#         # return JsonResponse({'data': product_serializer.data}, status=200)
#         return Response(product_serializer.data)
#     elif request.method == 'POST':
#         data = request.POST
#         product_serializer = ProductSerializer(data=data)
#         if product_serializer.is_valid():
#             new_product = product_serializer.save()
#             print(product_serializer.validated_data['category'])
#             return JsonResponse({'new_product_id': new_product.id}, status=201)
#         else:
#             return JsonResponse({'errors': product_serializer.errors}, status=400)
#     else:
#         return JsonResponse({}, status=405)


# class ProductApiSam(generics.RetrieveUpdateDestroyAPIView):
#     serializer_class = ProductSerializer
#     queryset = Product.objects.all()

class ProductListView(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'products/products_list.html')

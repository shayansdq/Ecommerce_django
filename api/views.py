from api.serializers import ProductsSerializer
from products.models import Product
from rest_framework import generics


class ProductList(generics.ListAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductsSerializer


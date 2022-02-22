from django.urls import path
# from .views import product_list_api, ProductApiSam
from .views import ProductListView

app_name = 'products'
urlpatterns = [
    path('', ProductListView.as_view(), name='products_list')
]

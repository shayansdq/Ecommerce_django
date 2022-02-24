from django.urls import path, include
from . import views

app_name = 'orders'

urlpatterns = [
    path('send-order/', views.CreateOrderView.as_view(), name='send_order')
]

from django.urls import path
from .views import *

urlpatterns = [
    path('list_products/',ProductList.as_view(), name='products_list'),
    # path('list_agents/',AgentsList, name='agents_list'),
    # path('list_services/',ServicesList, name='services_list'),
    # path('list_bookings/',BookingsList, name='bookings_list'),
]

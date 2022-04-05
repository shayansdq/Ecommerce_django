from django.urls import path, include
from . import views
from . import api_views
app_name = 'orders'

urlpatterns = [
    path('send-order/', views.CreateOrderView.as_view(), name='send_order'),
    path('shopping_cart/', views.ShoppingCartView.as_view(), name='cart_detail'),
    path('cart-detail/', api_views.CartDetailApi.as_view(), name='api_cart_detail'),
    path('check-offcode/', views.CheckOutCart.as_view(), name='check_off_code'),
    path('submit-order/', views.SubmitOrder.as_view(), name='submit_order'),
    path('load-cartitem/', api_views.LoadCartItemApi.as_view(), name='load_cart_items'),
]

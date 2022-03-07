from django.urls import path
from . import views

app_name = 'customers'

urlpatterns = [
    path('contact/', views.ContactUsView.as_view(), name='contact_view'),
    path('login-register/', views.LoginRegisterView.as_view(), name='register_login_view'),
    path('login/', views.LoginPostView.as_view(), name='do_login'),
    path('logout/', views.UserLogoutView.as_view(), name='logout'),
    path('reset/', views.UserPasswordResetView.as_view(), name='reset_password'),
    path('reset/done/', views.UserPasswordResetDoneView.as_view(), name='password_reset_done'),
    path('confirm/<uidb64>/<token>', views.UserPasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('confirm/complete', views.UserPasswordResetCompleteView.as_view(), name='password_reset_complete'),
    path('profile/', views.CustomerProfileView.as_view(), name='profile'),
    # path('address/<int:pk>', views.AddressDetailApi.as_view(), name='address_detail'),
    path('addresses/', views.AddressListApi.as_view(), name='address_list'),

]

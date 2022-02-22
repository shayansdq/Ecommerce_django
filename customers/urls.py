from django.urls import path
from . import views

app_name = 'customers'

urlpatterns = [
    path('contact/', views.ContactUsView.as_view(), name='contact_view'),
    path('login-register/', views.LoginRegisterView.as_view(), name='register_login_view'),
    path('login/', views.LoginPostView.as_view(), name='do_login'),
    path('logout/', views.UserLogoutView.as_view(), name='logout'),
]

from django.urls import path
from . import views

urlpatterns = [
    path('contact/', views.ContactUsView.as_view(), name='contact_view'),
    path('login-register/', views.LoginRegisterView.as_view(), name='register_login_view'),
    path('login/', views.LoginPostView.as_view(), name='do_login'),
]

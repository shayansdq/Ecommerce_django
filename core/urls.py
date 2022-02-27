from django.urls import path
from . import views

app_name = 'core'

urlpatterns = [
    path('about/',views.AboutPageView.as_view(),name='about_page')
]
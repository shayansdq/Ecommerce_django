from django.shortcuts import render
from django.views import View


# Create your views here.
from orders.models import CartItem


class AboutPageView(View):
    def get(self, request, *args, **kwargs):
        CartItem.remove_loaded_items_key(request)
        return render(request, 'core/about.html')


class ContactPageView(View):
    def get(self, request, *args, **kwargs):
        CartItem.remove_loaded_items_key(request)
        return render(request, 'core/contact.html')

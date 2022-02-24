from django.shortcuts import render
from django.views import View
from django.views import View


# Create your views here.

class CreateOrderView(View):
    def post(self, request, *args, **kwargs):
        print(request.POST)
        print(type(request.POST))

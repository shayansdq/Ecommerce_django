from django.shortcuts import render
from django.views import View


# Create your views here.


class AboutPageView(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'core/about.html')

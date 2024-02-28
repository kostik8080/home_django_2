from django.shortcuts import render
from django.views.generic import ListView, DetailView, TemplateView

from .models import Product, Category


class ProductListView(ListView):
    model = Product
    extra_context = {'title': 'Главная'}

class ContactView(TemplateView):
    template_name = 'catalog/contact.html'



class ProductDatailView(DetailView):
    model = Product




# def product(request, pk):
#     category_item = Category.objects.get(pk=pk)
#
#
#     context = {
#         'object_list': Product.objects.filter(category_id=pk),
#         'title': category_item.name
#
#     }
#     return render(request, 'catalog/product_detail.html', context)

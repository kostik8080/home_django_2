from django.shortcuts import render
from django.http import HttpResponse
from .models import Product
from django.template.loader import render_to_string

def index(request):
    products = Product.objects.order_by('-id')[:5]
    data_list = []
    for product in products:
        data_list.append(product.name)

    return render(request, 'catalog/index.html', {'products': data_list})


def contact(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        phone = request.POST.get('phone')
        message = request.POST.get('message')
        print(f"{name} ({phone}): {message}")
    return render(request, 'catalog/contact.html')



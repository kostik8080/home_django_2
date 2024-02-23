from django.shortcuts import render

from .models import Product, Category


def index(request):
    products = Product.objects.all()

    context = {
        'object_list': products,
        'title': 'Главная'

    }
    return render(request, 'catalog/index.html', context)


def contact(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        phone = request.POST.get('phone')
        message = request.POST.get('message')
        print(f"{name} ({phone}): {message}")
    context = {

        'title': 'Контакты'

    }
    return render(request, 'catalog/contact.html', context)


def product(request, pk):
    category_item = Category.objects.get(pk=pk)


    context = {
        'object_list': Product.objects.filter(category_id=pk),
        'title': category_item.name

    }
    return render(request, 'catalog/product.html', context)

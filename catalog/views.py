from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse, reverse_lazy
from pytils.translit import slugify
from django.views.generic import ListView, DetailView, TemplateView, CreateView, UpdateView, DeleteView

from .models import Product, Category


class ProductListView(ListView):
    model = Product
    extra_context = {'title': 'Главная'}


class ContactView(TemplateView):
    template_name = 'catalog/contact.html'


class ProductDatailView(DetailView):
    model = Product






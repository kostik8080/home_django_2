from django.forms import inlineformset_factory
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse, reverse_lazy
from pytils.translit import slugify
from django.views.generic import ListView, DetailView, TemplateView, CreateView, UpdateView, DeleteView

from .forms import ProductForm, VersionForm
from .models import Product, Category, Version


class ProductListView(ListView):
    model = Product
    extra_context = {'title': 'Главная'}

    # def get_queryset(self):
    #     queryset = super().get_queryset()
    #     queryset = queryset.filter(category_id=self.kwargs.get('pk'))
    #     return queryset
    #
    # def get_context_data(self, *args, **kwargs):
    #     context_data = super().get_context_data(*args, **kwargs)
    #     category_data = Category.objects.get(pk=self.kwargs.get('pk'))
    #     context_data['category_pk'] = category_data.pk
    #     context_data['title'] = f'{category_data.name}'
    #     for product in context_data.get('object_list'):
    #         product.version = product.version_set.filter(current_version=True).first()
    #     return context_data

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        products = Product.objects.all()

        for product in products:
            versions = Version.objects.filter(product=product)
            active_version = versions.filter(current_version=True).first()
            product.active_version = active_version.name_version if active_version else 'Версия неактивна'

        context['products'] = products

        return context


class ContactView(TemplateView):
    template_name = 'catalog/contact.html'


class ProductDatailView(DetailView):
    model = Product


class ProductCreateView(CreateView):
    model = Product
    form_class = ProductForm
    success_url = reverse_lazy('catalog:index')


class ProductUpdateView(UpdateView):
    model = Product
    form_class = ProductForm

    def get_success_url(self):
        return reverse('catalog:product_update', args=[self.kwargs.get('pk')])

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)
        VersionFormSet = inlineformset_factory(Product, Version, form=VersionForm, extra=1)
        if self.request.method == 'POST':
            formset = VersionFormSet(self.request.POST, instance=self.object)
        else:
            formset = VersionFormSet(instance=self.object)
        context_data['formset'] = formset
        return context_data

    def form_valid(self, form):
        context_data = self.get_context_data()
        formset = context_data['formset']
        self.object = form.save()
        if formset.is_valid():
            formset.instance = self.object
            formset.save()
        return super().form_valid(form)

class ProductDeleteView(DeleteView):
    model = Product
    success_url = reverse_lazy('catalog:index')



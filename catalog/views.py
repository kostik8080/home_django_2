from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.forms import inlineformset_factory, formset_factory
from django.http import request, Http404
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse, reverse_lazy
from django.views import View
from pytils.translit import slugify
from django.views.generic import ListView, DetailView, TemplateView, CreateView, UpdateView, DeleteView
from django.db.models import Q
from .forms import VersionForm, ProductForm1, ProductForm2
from .models import Product, Category, Version
from django.core.exceptions import PermissionDenied
from django.utils.decorators import method_decorator


class ProductListView(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    model = Product
    extra_context = {'title': 'Главная'}
    permission_required = 'catalog.view_product'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        products = Product.objects.all()

        for product in products:
            versions = Version.objects.filter(product=product)
            active_version = versions.filter(current_version=True).first()
            product.active_version = active_version.name_version if active_version else 'Версия неактивна'

        context['products'] = products

        return context


class ContactView(LoginRequiredMixin, PermissionRequiredMixin, TemplateView):
    template_name = 'catalog/contact.html'
    permission_required = 'catalog.view_product'


class ProductDatailView(LoginRequiredMixin, PermissionRequiredMixin, DetailView):
    model = Product
    permission_required = 'catalog.view_product'


class ProductCreateView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    model = Product
    form_class = ProductForm1
    permission_required = 'catalog.add_product'
    success_url = reverse_lazy('catalog:index')

    def form_valid(self, form):
        user_name = form.save()
        user_name.users = self.request.user
        user_name.save()
        return super().form_valid(form)


class UserPermissionMixin(View):
    @property
    def get_permiss(self):
        if self.request.user.is_staff:
            item_object = ('catalog.change_product', 'catalog.set_is_published', 'catalog.change_discription', 'catalog.change_category')
            return item_object
        if self.request.user.is_active and not self.request.user.is_superuser and not self.request.user.is_staff:
            item_object = 'catalog.change_product'
            return item_object


class ProductUpdateView(LoginRequiredMixin, PermissionRequiredMixin, UserPermissionMixin, UpdateView):
    model = Product
    form_class = ProductForm1

    permission_required = UserPermissionMixin.get_permiss


    def get_success_url(self):
        return reverse('catalog:product_update', args=[self.kwargs.get('pk')])

    def get_form_class(self):
        if len(self.permission_required) == 4:
            if self.request.user.has_perms(perm_list=self.permission_required) and not self.request.user.is_superuser:
                return ProductForm2
            else:
                return ProductForm1
        else:
            return ProductForm1



    def get_context_data(self, **kwargs):
        # Получение базового контекста с помощью super()
        global queryset
        context_data = super().get_context_data(**kwargs)

        # Создание формсета
        VersionFormSet = inlineformset_factory(Product, Version, form=VersionForm, extra=1)

        if self.request.method == 'POST':

            formset = VersionFormSet(self.request.POST, instance=self.object)
        else:
            # Если запрос GET, создаем пустой формсет
            formset = VersionFormSet(instance=self.object)

        # Добавление формсета в контекст
        context_data['formset'] = formset

        return context_data

    def form_valid(self, form):
        # Получение контекста данных
        context_data = self.get_context_data()
        formset = context_data['formset']

        # Сохранение основной формы
        self.object = form.save()

        if formset.is_valid():
            formset.instance = self.object
            formset.save()

        return super().form_valid(form)


class ProductDeleteView(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    model = Product
    permission_required = 'catalog.delete_product'
    success_url = reverse_lazy('catalog:index')

from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin, UserPassesTestMixin
from django.contrib.auth.models import Permission
from django.forms import inlineformset_factory, formset_factory
from django.http import request, Http404, HttpResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse, reverse_lazy
from django.views import View
from pytils.translit import slugify
from django.views.generic import ListView, DetailView, TemplateView, CreateView, UpdateView, DeleteView
from django.db.models import Q
from .forms import VersionForm, ProductFormCatalog, ProductFormAllUser
from .models import Product, Category, Version
from django.core.exceptions import PermissionDenied
from django.utils.decorators import method_decorator

from .services import get_cached_subjects_category


class ProductListView(LoginRequiredMixin, ListView):
    """ Представление для списка продуктов """
    model = Product
    extra_context = {'title': 'Главная'}

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        products = Product.objects.all()

        for product in products:
            versions = Version.objects.filter(product=product)
            active_version = versions.filter(current_version=True).first()
            product.active_version = active_version.name_version if active_version else 'Версия неактивна'

        context['products'] = products

        return context


class ContactView(LoginRequiredMixin, TemplateView):
    """ Представление для отправки сообщения """
    template_name = 'catalog/contact.html'


class ProductDatailView(LoginRequiredMixin, DetailView):
    """ Представление для просмотра продукта """
    model = Product


class ProductCreateView(LoginRequiredMixin, CreateView):
    """ Представление для создания продукта """
    model = Product
    form_class = ProductFormCatalog

    success_url = reverse_lazy('catalog:index')

    def form_valid(self, form):
        user_name = form.save()
        user_name.users = self.request.user
        user_name.save()
        return super().form_valid(form)


class ProductUpdateView(LoginRequiredMixin, UpdateView):
    """Представление для редактирования продукта
    наследуется от Product и при наличии прав на редактирование продукта проверяется
    если обычный пользователь и он владелец продукта он может редактировать, если администратор выводит форму редактирования
    только по определенным полям"""
    model = Product
    form_class = ProductFormCatalog

    permission_required = ('catalog.change_product', 'catalog.set_is_published', 'catalog.change_discription',
                           'catalog.change_category')

    def get_success_url(self):
        return reverse('catalog:product_update', args=[self.kwargs.get('pk')])

    def get_form_class(self):
        """Получение формы для редактирования продукта"""
        if self.request.user.is_staff and self.request.user.has_perms(
                perm_list=self.permission_required) and not self.request.user.is_superuser:
            return ProductFormAllUser
        elif self.request.user.is_superuser and self.request.user.has_perm('catalog.change_product'):
            return ProductFormCatalog
        else:
            if self.request.user.is_active and self.request.user.has_perm('catalog.change_product'):
                if self.request.user != self.get_object().users and self.request.user.is_active:
                    raise PermissionDenied

                return ProductFormCatalog

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
    """Представление для удаления продукта
    наследуется от Product и при наличии прав на удаление продукта вызывается PermissionRequiredMixin"""
    model = Product
    permission_required = 'catalog.delete_product'
    success_url = reverse_lazy('catalog:index')


class CategoryListView(LoginRequiredMixin, ListView):
    """Представление для списка категорий"""
    model = Category

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)
        context_data['subjects'] = get_cached_subjects_category()
        return context_data


def fobidden_view403(request, exception):
    return render(request, 'catalog/access_denied.html', status=403)

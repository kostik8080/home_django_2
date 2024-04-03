from django.urls import path
from django.views.decorators.cache import cache_page
from django.views.generic import TemplateView

from catalog.apps import MainConfig
from catalog.views import ProductListView, ProductDatailView, ContactView, ProductCreateView, ProductDeleteView, CategoryListView, ProductUpdateView

app_name = MainConfig.name

urlpatterns = [

    path('', ProductListView.as_view(), name="index"),
    path('contacts/', ContactView.as_view(), name="contacts"),
    path('category/', CategoryListView.as_view(), name="category"),
    path('product/<int:pk>/', cache_page(60)(ProductDatailView.as_view()), name="product_detail"),
    path('product/create/', ProductCreateView.as_view(), name="product_create"),
    path('product/update/<int:pk>/', ProductUpdateView.as_view(), name="product_update"),
    path('product/delete/<int:pk>/', ProductDeleteView.as_view(), name="product_delete"),

]
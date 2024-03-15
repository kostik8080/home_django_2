from django.urls import path

from catalog.apps import MainConfig
from catalog.views import ProductListView, ProductDatailView, ContactView, ProductCreateView, ProductDeleteView, ProductUpdateView

app_name = MainConfig.name

urlpatterns = [

    path('', ProductListView.as_view(), name="index"),
    path('contacts/', ContactView.as_view(), name="contacts"),
    path('product/<int:pk>/', ProductDatailView.as_view(), name="product_detail"),
    path('product/create/', ProductCreateView.as_view(), name="product_create"),
    path('product/update/<int:pk>/', ProductUpdateView.as_view(), name="product_update"),
    path('product/delete/<int:pk>/', ProductDeleteView.as_view(), name="product_delete"),
]
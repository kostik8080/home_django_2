from django.urls import path

from catalog.apps import MainConfig
from catalog.views import ProductListView, ProductDatailView, ContactView

app_name = MainConfig.name

urlpatterns = [
    path('', ProductListView.as_view(), name="index"),
    path('contacts/', ContactView.as_view(), name="contacts"),
    path('product/<int:pk>', ProductDatailView.as_view(), name="product_detail"),

]
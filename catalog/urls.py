from django.urls import path

from catalog.apps import MainConfig
from catalog.views import ProductListView, ProductDatailView, ContactView, BlogListView, BlogCreateView, BlogDetailView, BlogUpdateView, BlogDeleteView, activates

app_name = MainConfig.name

urlpatterns = [
    path('create/', BlogCreateView.as_view(), name="blog_create"),
    path('', ProductListView.as_view(), name="index"),
    path('contacts/', ContactView.as_view(), name="contacts"),
    path('product/<int:pk>', ProductDatailView.as_view(), name="product_detail"),
    path('blog/', BlogListView.as_view(), name="blog_list"),
    path('blog/<int:pk>', BlogDetailView.as_view(), name="blog_detail"),
    path('edit/<int:pk>', BlogUpdateView.as_view(), name="blog_update"),
    path('delete/<int:pk>', BlogDeleteView.as_view(), name="blog_delete"),
    path('activate/<int:pk>', activates, name="blog_activate"),
]
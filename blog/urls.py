from django.urls import path

from blog.apps import BlogConfig
from blog.views import BlogListView, BlogCreateView, BlogDetailView, BlogUpdateView, BlogDeleteView, activates

app_name = BlogConfig.name

urlpatterns = [
    path('create/', BlogCreateView.as_view(), name="blog_create"),
    path('', BlogListView.as_view(), name="blog_list"),
    path('blog/<int:pk>', BlogDetailView.as_view(), name="blog_detail"),
    path('edit/<int:pk>', BlogUpdateView.as_view(), name="blog_update"),
    path('delete/<int:pk>', BlogDeleteView.as_view(), name="blog_delete"),
    path('activate/<int:pk>', activates, name="blog_activate"),

]



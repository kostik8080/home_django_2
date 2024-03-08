from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy, reverse
from django.views.generic import ListView, CreateView, DetailView, UpdateView, DeleteView
from pytils.translit import slugify

from blog.models import Blog


class BlogListView(ListView):
    model = Blog

    def get_queryset(self, *args, **kwargs):
        queryset = super().get_queryset(*args, **kwargs)
        queryset = queryset.filter(is_published=True)
        return queryset



class BlogCreateView(CreateView):
    model = Blog
    fields = ('title', 'content', 'slug', 'photo',)
    success_url = reverse_lazy('catalog:blog_list')

    def form_valid(self, form):
        if form.is_valid():
            new_mat = form.save()
            new_mat.slug = slugify(new_mat.title)
            new_mat.save()

        return super().form_valid(form)





class BlogDetailView(DetailView):
    model = Blog

    def get_object(self, queryset=None):
        self.object = super().get_object(queryset)
        self.object.count_views += 1
        self.object.save()
        return self.object


class BlogUpdateView(UpdateView):
    model = Blog
    fields = ('title', 'content', 'slug', 'photo',)
    #success_url = reverse_lazy('catalog:blog_detail')



    def get_success_url(self):
        return reverse('catalog:blog_detail', args=[self.kwargs.get('pk')])


class BlogDeleteView(DeleteView):
    model = Blog
    success_url = reverse_lazy('catalog:blog_list')


def activates(request, pk):
    blogs_item = get_object_or_404(Blog, pk=pk)
    if blogs_item.is_published:
        blogs_item.is_published = False
    else:
        blogs_item.is_published = True
    blogs_item.save()
    return redirect(reverse('blog:blog_list'))

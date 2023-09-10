from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy, reverse
from django.views.generic import CreateView, ListView, DetailView, UpdateView, DeleteView
from pytils.translit import slugify

from blog.models import Article


class ArticleCreateView(CreateView):
    model = Article
    fields = ('title', 'content', 'preview', 'is_published')
    success_url = reverse_lazy('blog:article_list')

    def form_valid(self, form):
        if form.is_valid():
            new_material = form.save()
            new_material.slug = slugify(new_material.title)
            new_material.save()
        return super().form_valid(form)


class ArticleListView(ListView):
    model = Article

    def get_queryset(self):
        queryset = super().get_queryset()
        queryset = queryset.filter(is_published=True)
        return queryset


def unpublished_articles(request):
    unpublished = Article.objects.filter(is_published=False)
    context = {'object_list': unpublished}
    return render(request, 'blog/article_list.html', context)


class ArticleDetailView(DetailView):
    model = Article

    def get_object(self, queryset=None):
        self.object = super().get_object()
        self.object.views_count += 1
        self.object.save()
        return self.object


def toggle_publication(request, slug):
    article_item = get_object_or_404(Article, slug=slug)  # получаем объект или ошибку 404
    if article_item.is_published:
        article_item.is_published = False
        article_item.save()
        return redirect(reverse('blog:unpublished'))
    else:
        article_item.is_published = True
        article_item.save()
        return redirect(reverse('blog:article_list'))


class ArticleUpdateView(UpdateView):
    model = Article
    fields = ('title', 'content', 'preview')

    def get_success_url(self):
        return reverse('blog:article_detail', args=[self.kwargs.get('slug')])


class ArticleDeleteView(DeleteView):
    model = Article
    success_url = reverse_lazy('blog:article_list')

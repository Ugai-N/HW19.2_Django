from django.urls import reverse_lazy
from django.views.generic import CreateView, ListView, DetailView, UpdateView, DeleteView

from blog.models import Article


class ArticleCreateView(CreateView):
    model = Article
    fields = ('title', 'content', 'preview')
    extra_context = {'title': 'Vardikova & Co'}
    success_url = reverse_lazy('blog:article_list')


class ArticleListView(ListView):
    model = Article


class ArticleDetailView(DetailView):
    model = Article


class ArticleUpdateView(UpdateView):
    model = Article
    success_url = reverse_lazy('blog:article_list')


class ArticleDeleteView(DeleteView):
    model = Article
    success_url = reverse_lazy('blog:article_list')

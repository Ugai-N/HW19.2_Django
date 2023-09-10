from django.urls import path

from blog.apps import BlogConfig
from blog.views import ArticleCreateView, ArticleListView, ArticleDetailView, ArticleUpdateView, ArticleDeleteView, \
    unpublished_articles, toggle_publication

app_name = BlogConfig.name

urlpatterns = [
    path('', ArticleListView.as_view(), name='article_list'),
    path('view/<slug:slug>', ArticleDetailView.as_view(), name='article_detail'),
    path('add/', ArticleCreateView.as_view(), name='add_article'),
    path('edit/<slug:slug>', ArticleUpdateView.as_view(), name='edit_article'),
    path('delete/<slug:slug>', ArticleDeleteView.as_view(), name='delete_article'),
    path('unpublished/', unpublished_articles, name='unpublished'),
    path('publication/<slug:slug>', toggle_publication, name='toggle_publication'),
]

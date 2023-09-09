from django.urls import path

from blog.apps import BlogConfig
from blog.views import ArticleCreateView, ArticleListView, ArticleDetailView, ArticleUpdateView, ArticleDeleteView

app_name = BlogConfig.name

urlpatterns = [
    path('', ArticleListView.as_view(), name='article_list'),
    path('view/<int:pk>', ArticleDetailView.as_view(), name='article_detail'),
    path('add/', ArticleCreateView.as_view(), name='add_article'),
    path('edit/<int:pk>', ArticleUpdateView.as_view(), name='edit_article'),
    path('delete/<int:pk>', ArticleDeleteView.as_view(), name='delete_article'),
]

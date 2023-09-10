from django.contrib import admin

from blog.models import Article


@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    list_display = ('pk', 'title', 'preview', 'created_at', 'is_published', 'views_count', 'slug')
    list_filter = ('is_published', 'created_at',)
    search_fields = ('title', 'content',)
    prepopulated_fields = {"slug": ("title",)}

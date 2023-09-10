from django.db import models

NULLABLE = {'blank': True, 'null': True}


class Article(models.Model):
    title = models.CharField(max_length=250, verbose_name='заголовок')
    slug = models.CharField(max_length=250, verbose_name='slug')
    content = models.TextField(verbose_name='содержимое')
    preview = models.ImageField(verbose_name='превью', **NULLABLE)
    created_at = models.DateField(auto_now_add=True, verbose_name='дата_создания')
    is_published = models.BooleanField(default=True, verbose_name='опубликовано')
    views_count = models.IntegerField(default=0, verbose_name='просмотры')

    def __str__(self):
        return f'{self.title} ' \
               f'({self.is_published.verbose_name if self.is_published else "не опубликовано"})'

    class Meta:
        verbose_name = 'статья'
        verbose_name_plural = 'статьи'
        ordering = ('views_count', 'title', 'created_at',)

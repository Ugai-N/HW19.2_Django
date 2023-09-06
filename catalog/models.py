from django.db import models

NULLABLE = {'blank': True, 'null': True}


class Product(models.Model):
    """Класс для товаров"""
    title = models.CharField(max_length=100, verbose_name='Наименование')
    description = models.TextField(max_length=1000, verbose_name='Описание', **NULLABLE)
    pic = models.ImageField(upload_to='pics/', verbose_name='Превью', **NULLABLE)
    price = models.IntegerField(verbose_name='Цена')
    created_at = models.DateField(auto_now_add=True, verbose_name='Дата создания', **NULLABLE)
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Дата изменения', **NULLABLE)
    category = models.ForeignKey('Category', on_delete=models.CASCADE, verbose_name='Категория')

    def __str__(self):
        return f'{self.title}: {self.price}'

    class Meta:
        verbose_name = 'Товар'
        verbose_name_plural = 'Товары'
        ordering = ('title', 'price',)


class Category(models.Model):
    """Класс для категорий товаров"""
    title = models.CharField(max_length=100, verbose_name='Наименование')
    description = models.TextField(max_length=1000, verbose_name='Описание', **NULLABLE)

    def __str__(self):
        return f'{self.title}'

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'
        ordering = ('title',)


class Contacts(models.Model):
    """Класс для контакных данных компании"""
    country = models.CharField(max_length=100, verbose_name='Страна')
    tax_id = models.IntegerField(verbose_name='ИНН')
    address = models.CharField(max_length=100, verbose_name='Адрес')

    def __str__(self):
        return f'{self.address} ({self.country})'

    class Meta:
        verbose_name = 'Контакты'

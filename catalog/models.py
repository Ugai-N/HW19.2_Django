from django.db import models

NULLABLE = {'blank': True, 'null': True}


class Product(models.Model):
    title = models.CharField(max_length=100, verbose_name='Наименование')
    description = models.TextField(max_length=1000, verbose_name='Описание', **NULLABLE)
    pic = models.ImageField(upload_to='pics/', verbose_name='Превью', **NULLABLE)
    price = models.IntegerField(verbose_name='Цена')
    create_date = models.DateField(verbose_name='Дата создания', **NULLABLE)
    change_date = models.DateField(verbose_name='Дата изменения', **NULLABLE)
    category = models.ForeignKey('Category', on_delete=models.CASCADE, verbose_name='Категория')

    def __str__(self):
        return f'{self.title}: {self.price}'

    class Meta:
        verbose_name = 'Товар'
        verbose_name_plural = 'Товары'
        ordering = ('title', 'price',)


class Category(models.Model):
    title = models.CharField(max_length=100, verbose_name='Наименование')
    description = models.TextField(max_length=1000, verbose_name='Описание', **NULLABLE)
    # created_at = models.DateField(verbose_name='дата', **NULLABLE)

    def __str__(self):
        return f'{self.title}'

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'
        ordering = ('title',)

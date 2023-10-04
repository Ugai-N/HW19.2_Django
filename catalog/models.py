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
    owner = models.ForeignKey('users.User', on_delete=models.CASCADE, **NULLABLE, verbose_name='Владелец')

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


class Version(models.Model):
    """Класс для версии товара"""
    title = models.CharField(max_length=100, verbose_name='Название')
    num = models.IntegerField(verbose_name='Номер')
    # num = models.IntegerField(verbose_name='Номер', default=1, auto_created=True)
    created_at = models.DateField(auto_now_add=True, verbose_name='Дата создания')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Дата изменения')
    product = models.ForeignKey('Product', on_delete=models.CASCADE, verbose_name='Товар')
    # is_active = models.CharField(verbose_name='Текущая', choices=(('YES', 'ДА'), ('NO', 'НЕТ')), default='NO')
    is_active = models.BooleanField(verbose_name='Текущая', default=False)

    def __str__(self):
        return f'{self.title}({self.product.title})'

    class Meta:
        verbose_name = 'Версия'
        verbose_name_plural = 'Версии'
        ordering = ('is_active',)


class Contacts(models.Model):
    """Класс для контакных данных компании"""
    country = models.CharField(max_length=100, verbose_name='Страна')
    tax_id = models.IntegerField(verbose_name='ИНН')
    address = models.CharField(max_length=100, verbose_name='Адрес')

    def __str__(self):
        return f'{self.address} ({self.country})'

    class Meta:
        verbose_name = 'Контакты'

from django.conf import settings
from django.core.cache import cache

from catalog.models import Version, Product, Category


def get_products_with_active_versions(*queryset):
    queryset = queryset[0] if queryset else Product.objects.all()
    active_versions = Version.objects.filter(is_active=True)
    active_products = [version.product.pk for version in active_versions]
    queryset = queryset.filter(pk__in=active_products)
    return queryset


def get_category_products(category_pk):
    return Product.objects.filter(category_id=category_pk)


def get_categories_list():
    if settings.CACHE_ENABLED:
        key = 'categories_list'
        categories_list = cache.get(key)
        if categories_list is None:
            categories_list = Category.objects.all()
            cache.set(key, categories_list)
    else:
        categories_list = Category.objects.all()
    return categories_list

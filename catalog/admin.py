from django.contrib import admin

from catalog.models import Product, Category, Contacts


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('pk', 'title', 'price', 'category', 'created_at', 'updated_at', 'pic')
    list_filter = ('category',)
    search_fields = ('title', 'description',)


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('pk', 'title',)


@admin.register(Contacts)
class ContactsAdmin(admin.ModelAdmin):
    list_display = ('address', 'country',)

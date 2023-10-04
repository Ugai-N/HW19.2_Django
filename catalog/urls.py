from django.urls import path
from django.views.decorators.cache import cache_page, never_cache

from catalog.apps import CatalogConfig
from catalog.views import ProductCreateView, ProductDetailView, category_products, ProductListView, contacts, \
    ProductUpdateView, ProductDeleteView

app_name = CatalogConfig.name

urlpatterns = [
    path('', ProductListView.as_view(), name='index'),
    path('contacts/', contacts, name='contacts'),
    path('product/<int:pk>', cache_page(60)(ProductDetailView.as_view()), name='product'),
    path('category/<int:pk>', category_products, name='category_products'),
    path('product/add/', never_cache(ProductCreateView.as_view()), name='add_product'),
    path('product/<int:pk>/update/', never_cache(ProductUpdateView.as_view()), name='edit_product'),
    path('product/<int:pk>/delete/', ProductDeleteView.as_view(), name='delete_product'),
]

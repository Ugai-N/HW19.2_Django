from django.urls import path

from catalog.apps import CatalogConfig
from catalog.views import ProductCreateView, ProductDetailView, category_products, ProductListView, contacts, \
    ProductUpdateView, ProductDeleteView

app_name = CatalogConfig.name

urlpatterns = [
    path('', ProductListView.as_view(), name='index'),
    path('contacts/', contacts, name='contacts'),
    path('product/<int:pk>', ProductDetailView.as_view(), name='product'),
    path('category/<int:pk>', category_products, name='category_products'),
    path('product/add/', ProductCreateView.as_view(), name='add_product'),
    path('product/<int:pk>/update/', ProductUpdateView.as_view(), name='edit_product'),
    path('product/<int:pk>/delete/', ProductDeleteView.as_view(), name='delete_product'),
]

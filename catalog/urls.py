from django.urls import path

from catalog.apps import CatalogConfig
from catalog.views import index, contacts, product, category

app_name = CatalogConfig.name

urlpatterns = [
    path('', index, name='index'),
    path('contacts/', contacts, name='contacts'),
    path('<int:pk> /product/', product, name='product'),
    path('<int:pk> /category/', category, name='category'),
]

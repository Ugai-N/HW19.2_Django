from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import CreateView, DetailView, ListView

from catalog.models import Product, Contacts, Category


class ProductListView(ListView):
    paginate_by = 3
    model = Product
    extra_context = {'title': 'Vardikova & Co',
                     'add_title': 'Психологическая помощь на разные случаи жизни в вашем кармане'}


def contacts(request):
    """Обработка POST запроса на странице /contacts+
    передает в шаблон contacts данные модели Contacts"""

    str_address = Contacts.objects.get(pk=1)
    context = {"tax": str_address.tax_id, "address": str_address.address, "country": str_address.country, 'title': "Контакты"}

    if request.method == "POST":
        name = request.POST.get('name')
        email = request.POST.get('email')
        message = request.POST.get('message')
        phone = request.POST.get('phone') if request.POST.get('phone') else None
        print(f"{name} ({email}, {phone}): {message}")
    return render(request, 'catalog/contacts_list.html', context)


class ProductDetailView(DetailView):
    model = Product
    extra_context = {'title': 'Vardikova & Co'}


def category_products(request, pk):
    """Обработка страницы с товарами определенной категорий
    ListView оставляем на Главную index, здесь будто логичнее оставить FBV.
    Но и ProductListView(CBV), и category_products(FBV) ссылаются на один шаблон product_list.html"""

    category_items = Product.objects.filter(category_id=pk)
    context = {"object_list": category_items, 'title': Category.objects.get(pk=pk),
               'add_title': 'Психологическая помощь на разные случаи жизни в вашем кармане'}
    return render(request, 'catalog/product_list.html', context)


class ProductCreateView(CreateView):
    model = Product
    fields = ('title', 'description', 'pic', 'price', 'category')
    success_url = reverse_lazy('catalog:index')

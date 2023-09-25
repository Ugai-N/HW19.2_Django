from django.db import transaction
from django.forms import inlineformset_factory
from django.shortcuts import render
from django.urls import reverse_lazy, reverse
from django.views.generic import CreateView, DetailView, ListView, UpdateView, DeleteView

from catalog.forms import ProductForm, VersionForm
from catalog.models import Product, Contacts, Category, Version


class ProductListView(ListView):
    """вывод списка товаров только с активными версиями"""
    paginate_by = 3
    model = Product
    extra_context = {'title': 'Vardikova & Co',
                     'add_title': 'Психологическая помощь на разные случаи жизни в вашем кармане'}

    def get_queryset(self, *args, **kwargs):
        active_versions = Version.objects.filter(is_active='YES')
        active_products = [version.product.pk for version in active_versions]
        queryset = super().get_queryset(*args, **kwargs)
        queryset = queryset.filter(pk__in=active_products)
        return queryset


def contacts(request):
    """Обработка POST запроса на странице /contacts+
    передает в шаблон contacts данные модели Contacts"""

    str_address = Contacts.objects.get(pk=1)
    context = {"tax": str_address.tax_id, "address": str_address.address, "country": str_address.country,
               'title': "Контакты"}

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
    """Обработка страницы с товарами определенной категории только с активными версиями Товара"""

    active_versions = Version.objects.filter(is_active='YES')
    active_products = [version.product.pk for version in active_versions]
    category_items = Product.objects.filter(category_id=pk, pk__in=active_products)

    context = {"object_list": category_items, 'title': Category.objects.get(pk=pk),
               'add_title': 'Психологическая помощь на разные случаи жизни в вашем кармане'}
    return render(request, 'catalog/product_list.html', context)


class ProductCreateView(CreateView):
    model = Product
    form_class = ProductForm

    def get_success_url(self):
        return reverse('catalog:category_products', args=[self.object.category_id])


class ProductUpdateView(UpdateView):
    model = Product
    form_class = ProductForm

    def get_success_url(self):
        return reverse('catalog:product', args=[self.object.pk])

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)
        VersionFormset = inlineformset_factory(Product, Version, form=VersionForm, extra=1)
        if self.request.method == 'POST':
            context_data['formset'] = VersionFormset(self.request.POST, instance=self.object)
        else:
            context_data['formset'] = VersionFormset(instance=self.object)
        return context_data

    def form_valid(self, form):
        formset = self.get_context_data().get('formset')
        self.object = form.save()
        # with transaction.atomic():
        if formset.is_valid:
            formset.instance = self.object
            formset.save()
        return super().form_valid(form)


class ProductDeleteView(DeleteView):
    model = Product

    def get_success_url(self):
        return reverse('catalog:category_products', args=[self.object.category_id])

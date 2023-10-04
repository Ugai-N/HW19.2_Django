from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, AccessMixin, UserPassesTestMixin
from django.forms import inlineformset_factory
from django.shortcuts import render, redirect
from django.urls import reverse_lazy, reverse
from django.views.generic import CreateView, DetailView, ListView, UpdateView, DeleteView, TemplateView

from catalog.forms import ProductForm, VersionForm, VersionBaseInLineFormSet
from catalog.models import Product, Contacts, Category, Version
from catalog.services import get_category_products, \
    get_products_with_active_versions, get_categories_list


# надо установить кастомное право автора-владельца
class OwnerRequiredMixin(AccessMixin):
    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return self.handle_no_permission()
        if request.user.is_authenticated:
            if not request.user.is_staff:
                # if request.user.pk != Product.objects.filter(pk=kwargs['pk'])[0].owner_id:
                if request.user.pk != self.get_object().owner:
                    messages.info(request, 'Изменение и удаление статьи доступно только автору')
                    return redirect('/users/')
        return super().dispatch(request, *args, **kwargs)


class ProductListView(LoginRequiredMixin, ListView):
    """вывод списка товаров только с активными версиями"""
    paginate_by = 3
    model = Product
    extra_context = {'title': 'Vardikova & Co',
                     'add_title': 'Психологическая помощь на разные случаи жизни в вашем кармане'}

    def get_queryset(self, *args, **kwargs):
        queryset = super().get_queryset(*args, **kwargs)
        queryset = get_products_with_active_versions(queryset)
        return queryset


def contacts(request):
    """Обработка POST запроса на странице /contacts+
    передает в шаблон contacts данные модели Contacts"""

    str_address = Contacts.objects.get(pk=1)
    context = {'tax': str_address.tax_id, 'address': str_address.address, 'country': str_address.country,
               'title': "Контакты"}

    if request.method == "POST":
        name = request.POST.get('name')
        email = request.POST.get('email')
        message = request.POST.get('message')
        phone = request.POST.get('phone') if request.POST.get('phone') else None
        print(f"{name} ({email}, {phone}): {message}")
    return render(request, 'catalog/contacts_list.html', context)


class ProductDetailView(LoginRequiredMixin, DetailView):
    model = Product
    extra_context = {'title': 'Vardikova & Co'}


@login_required
def category_products(request, pk):
    """Обработка страницы с товарами определенной категории только с активными версиями Товара"""

    products_in_category = get_category_products(pk)
    products_in_category = get_products_with_active_versions(products_in_category)

    context = {"object_list": products_in_category, 'title': Category.objects.get(pk=pk),
               'add_title': 'Психологическая помощь на разные случаи жизни в вашем кармане'}
    return render(request, 'catalog/product_list.html', context)


class ProductCreateView(LoginRequiredMixin, CreateView):
    model = Product
    form_class = ProductForm

    def get_success_url(self):
        return reverse('catalog:category_products', args=[self.object.category_id])

    def form_valid(self, form):
        if form.is_valid():
            form.instance.owner = self.request.user
            form.save()
        return super().form_valid(form)


# class ProductUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
class ProductUpdateView(OwnerRequiredMixin, UpdateView):
    model = Product
    form_class = ProductForm

    def get_success_url(self):
        return reverse('catalog:product', args=[self.object.pk])

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)
        VersionFormset = inlineformset_factory(Product, Version, form=VersionForm, extra=1,
                                               formset=VersionBaseInLineFormSet)
        if self.request.method == 'POST':
            context_data['formset'] = VersionFormset(self.request.POST, instance=self.object)
        else:
            context_data['formset'] = VersionFormset(instance=self.object)
        return context_data

    def form_valid(self, form):
        formset = self.get_context_data().get('formset')
        self.object = form.save()
        if formset.is_valid():
            formset.instance = self.object
            formset.save()
        else:
            error_message = formset.non_form_errors()  # собирает все ошибки формы
            messages.error(self.request, error_message)
            return self.form_invalid(form)
        return super().form_valid(form)

    # def test_func(self):
    #     return self.request.user.is_staff or self.request.user == self.get_object().owner


# class ProductDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
class ProductDeleteView(OwnerRequiredMixin, DeleteView):
    model = Product

    def get_success_url(self):
        return reverse('catalog:category_products', args=[self.object.category_id])

    # def test_func(self):
    #     return self.request.user.is_staff or self.request.user == self.get_object().owner

from django.shortcuts import render

from catalog.models import Product, Contacts, Category


# Create your views here.
def index(request):
    """Обработка запроса на главной странице+
    при переходе на главную страницу печатает в консоль 5 последних товаров"""

    # print(Product.objects.all()[::-1][:5])
    context = {'object_list': Product.objects.all(), 'title': 'Vardikova & Co'}
    return render(request, 'catalog/index.html', context)


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
    return render(request, 'catalog/contacts.html', context)


def product(request, pk):
    """Обработка страницы с одним товаром. Выводится из index или category
    Для перехода к след. или предыдущему товару используется тег next_pk и prev_pk соответственно"""

    item = Product.objects.get(pk=pk)
    context = {"object": item, 'title': 'Vardikova & Co'}
    return render(request, 'catalog/product.html', context)


def category(request, pk):
    """Обработка страницы с товарами определенной категорий"""

    category_items = Product.objects.filter(category_id=pk)
    context = {"object_list": category_items, 'title': Category.objects.get(pk=pk)}
    return render(request, 'catalog/category.html', context)


def add_item(request):
    """Обработка POST запроса на странице /add_item"""

    context = {'title': "Добавить новый товар"}
    if request.method == "POST":
        title = request.POST.get('title')
        description = request.POST.get('description') if request.POST.get('description') else None
        pic = request.POST.get('pic') if request.POST.get('pic') else None
        price = request.POST.get('price')
        category = Category(request.POST.get('category'))
        Product.objects.create(title=title, description=description, pic=pic, price=price, category=category)
    return render(request, 'catalog/add_item.html', context)

from django.shortcuts import render

from catalog.models import Product, Contacts


# Create your views here.
def index(request):
    """Обработка запроса на главной странице+
    при переходе на главную страницу печатает в консоль 5 последних товаров"""

    print(Product.objects.all()[::-1][:5])
    context = {'title': 'Vardikova & Co'}
    return render(request, 'catalog/index.html', context)


def contacts(request):
    """Обработка POST запроса на странице /contacts+
    передает в шаблон contacts данные модели Contacts"""

    str_address = Contacts.objects.get(pk=1)
    data = {"tax": str_address.tax_id, "address": str_address.address, "country": str_address.country, 'title': "Контакты"}
    if request.method == "POST":
        name = request.POST.get('name')
        email = request.POST.get('email')
        message = request.POST.get('message')
        phone = request.POST.get('phone') if request.POST.get('phone') else None
        print(f"{name} ({email}, {phone}): {message}")
    return render(request, 'catalog/contacts.html', context=data)

from django.shortcuts import render

# Create your views here.
def index(request):
    "Обработка запроса на главной странице"
    return render(request, 'catalog/index.html')


def contacts(request):
    "Обработка POST запроса на странице /contacts"
    if request.method == "POST":
        name = request.POST.get('name')
        email = request.POST.get('email')
        message = request.POST.get('message')
        phone = request.POST.get('phone') if request.POST.get('phone') else None
        print(f"{name} ({email}, {phone}): {message}")
    return render(request, 'catalog/contacts.html')

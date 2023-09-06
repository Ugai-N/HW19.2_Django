from django import template

from catalog.models import Product

register = template.Library()


@register.filter()
def next_pk(pk):
    lst = [item.pk for item in Product.objects.all()]
    new_index = lst.index(pk) + 1
    if new_index <= len(lst) - 1:
        return lst[new_index]
    else:
        return lst[0]


@register.filter()
def prev_pk(pk):
    lst = [item.pk for item in Product.objects.all()]
    new_index = lst.index(pk) - 1
    if new_index >= 0:
        return lst[new_index]
    else:
        return lst[len(lst) - 1]


@register.simple_tag()
def mymedia(value):
    if value:
        return f'/media/{value}'
    else:
        return ''

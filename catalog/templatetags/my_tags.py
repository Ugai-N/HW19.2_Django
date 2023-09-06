from django import template

from catalog.models import Product

register = template.Library()

@register.filter()
def next_pk(pk):
    new_pk = pk + 1
    try:
        Product.objects.get(pk=new_pk)
        return new_pk
    except Exception:
        return pk

@register.filter()
def prev_pk(pk):
    new_pk = pk - 1
    try:
        Product.objects.get(pk=new_pk)
        return new_pk
    except Exception:
        return pk


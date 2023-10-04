from django import forms
from django.forms import BaseInlineFormSet

from catalog.models import Product, Version

BANNED_PRODUCTS = ['казино', 'криптовалюта', 'крипта', 'биржа', 'дешево', 'бесплатно', 'обман', 'полиция', 'радар']

# class StyleFormMixin:
#     def __init__(self, *args, **kwargs):
#         super().__init__(*args, **kwargs)
#         for field_name, field in self.fields.items():
#             # field.widget.attrs['class'] = 'form-control'
#             if isinstance(field.widget, forms.widgets.CheckboxInput):
#                 field.widget.attrs['class'] = 'form-check-input'
#             elif isinstance(field.widget, forms.DateTimeInput):
#                 field.widget.attrs['class'] = 'form-control flatpickr-basic'
#             elif isinstance(field.widget, forms.DateInput):
#                 field.widget.attrs['class'] = 'form-control datepicker'
#             elif isinstance(field.widget, forms.TimeInput):
#                 field.widget.attrs['class'] = 'form-control flatpickr-time'
#             elif isinstance(field.widget, forms.widgets.SelectMultiple):
#                 field.widget.attrs['class'] = 'form-control select2 select2-multiple'
#             elif isinstance(field.widget, forms.widgets.Select):
#                 field.widget.attrs['class'] = 'form-control select2'
#             else:
#                 field.widget.attrs['class'] = 'form-control'


# class ProductForm(StyleFormMixin, forms.ModelForm):
class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        exclude = ('owner',)

    def clean(self):
        for word in BANNED_PRODUCTS:
            for word_var in [word.title(), word.upper(), word.lower()]:
                cleaned_title = self.cleaned_data['title']
                cleaned_description = self.cleaned_data['description']
                if word_var in cleaned_title or word_var in cleaned_description:
                    raise forms.ValidationError('Данный товар запрещен')
        return self.cleaned_data


# class VersionForm(StyleFormMixin, forms.ModelForm):
class VersionForm(forms.ModelForm):
    class Meta:
        model = Version
        # exclude = ('num',)
        fields = '__all__'


#  через clean поле номера переопределить-заполнить автоматически + скрыть


class VersionBaseInLineFormSet(BaseInlineFormSet):
    def clean(self):
        super().clean()
        current_ver_count = 0
        for form in self.forms:
            if form.cleaned_data.get('is_active'):    # form.cleaned_data = содержимое всей формы, есть формы пустые
                current_ver_count += 1
        if current_ver_count > 1:
            raise forms.ValidationError('Уже есть активная версия')

from django import forms
from django.forms import CheckboxInput, BaseInlineFormSet

from catalog.models import Product, Version

BANNED_PRODUCTS = ['казино', 'криптовалюта', 'крипта', 'биржа', 'дешево', 'бесплатно', 'обман', 'полиция', 'радар']


class StyleFormMixin:
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'
            # if field_name == 'is_active':
            #     widget = forms.CheckboxInput


class ProductForm(StyleFormMixin, forms.ModelForm):
    class Meta:
        model = Product
        # fields = '__all__'
        exclude = ('owner',)

    def clean(self):
        for word in BANNED_PRODUCTS:
            for word_var in [word.title(), word.upper(), word.lower()]:
                cleaned_title = self.cleaned_data['title']
                cleaned_description = self.cleaned_data['description']
                if word_var in cleaned_title or word_var in cleaned_description:
                    raise forms.ValidationError('Данный товар запрещен')


class VersionForm(StyleFormMixin, forms.ModelForm):
    # is_active = forms.BooleanField(widget=forms.CheckboxInput(attrs={'class': 'form-control'}))
    class Meta:
        model = Version
        # exclude = ('num',)
        fields = '__all__'

        # widgets = {
        #     'is_active': CheckboxInput(attrs={
        #         'class': 'form-control',
        #     }),
        # }

    # def clean(self):
    #     super().clean()
    #     product_versions_list = []
    #     for form in Product.objects.get(pk=self.cleaned_data['product'].pk).formset:
    #         product_versions_list.append(form.cleaned_data['is_active'])
    #     if product_versions_list.count('YES') > 1:
    #         raise forms.ValidationError('Уже есть активная версия')


# class VersionBaseInLineFormSet(BaseInlineFormSet):
#     def clean(self):
#         super().clean()
#         product_versions_list = [form.cleaned_data['is_active'] for form in self.forms if 'is_active' in form.cleaned_data]
#         if product_versions_list.count('YES') > 1:
#             raise forms.ValidationError('Уже есть активная версия')

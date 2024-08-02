from django import forms
from django.forms import ModelForm

from libs import CustomFormatter
from product.models import Product, ProductVersion


# ***** ФОРМА ТОВАРА *****
class ProductForm(ModelForm):
    forbidden_words = ("казино", "криптовалюта", "крипта", "биржа", "дешево", "бесплатно", "обман", "полиция", "радар")

    class Meta:
        model = Product
        fields = ('name', 'description', 'ava', 'price', 'category', 'is_published')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        CustomFormatter.format_form_fields(self)

    def clean_name(self):
        cleaned_name = self.cleaned_data["name"]
        ProductForm.find_forbidden_words("Название", cleaned_name)
        return cleaned_name

    def clean_description(self):
        cleaned_description = self.cleaned_data["description"]
        ProductForm.find_forbidden_words("Описание", cleaned_description)
        return cleaned_description

    @staticmethod
    def find_forbidden_words(field_name, value):
        """
            проверяет  поле на наличие запрещенных слов
            :param field_name: название поля
            :param value: значение поля
        """
        if value is None:
            return

        for word in ProductForm.forbidden_words:
            if word in value:
                raise forms.ValidationError(f"{field_name} имеет запрещенное слово \"{word}\"")


# ***** ФОРМА ВЕРСИИ ТОВАРА *****
class ProductVersionForm(ModelForm):
    class Meta:
        model = ProductVersion
        fields = ("name", "number", "product", "is_current")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        CustomFormatter.format_form_fields(self)

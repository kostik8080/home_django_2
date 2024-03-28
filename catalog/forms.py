from django import forms
from django.db.models import Q
from catalog.models import Product, Version


class StyleFormMixin:
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'
            if isinstance(field, forms.BooleanField):
                field.widget.attrs.update({'class': 'form-check-input'})


class ProductForm1(StyleFormMixin, forms.ModelForm):
    words = ['казино', 'криптовалюта', 'крипта', 'биржа', 'дешево', 'бесплатно', 'обман', 'полиция', 'радар']

    class Meta:
        model = Product
        # fields = '__all__'
        exclude = ['users']

    def clean_name(self):
        cleaned_data = self.cleaned_data['name']
        for word in self.words:
            if word in cleaned_data.lower():
                raise forms.ValidationError('Нельзя использовать слово ' + word)
        return cleaned_data

    def clean_description(self):
        cleaned_data = self.cleaned_data['description']
        for word in self.words:
            if word in cleaned_data.lower():
                raise forms.ValidationError('Нельзя использовать слово ' + word)
        return cleaned_data


class ProductForm2(StyleFormMixin, forms.ModelForm):
    words = ['казино', 'криптовалюта', 'крипта', 'биржа', 'дешево', 'бесплатно', 'обман', 'полиция', 'радар']

    class Meta:
        model = Product
        fields = ('description', 'category', 'is_published')

    def clean_description(self):
        cleaned_data = self.cleaned_data['description']
        for word in self.words:
            if word in cleaned_data.lower():
                raise forms.ValidationError('Нельзя использовать слово ' + word)
        return cleaned_data


class VersionForm(StyleFormMixin, forms.ModelForm):
    class Meta:
        model = Version
        fields = '__all__'

    def clean_current_version(self):
        active_version = []
        version = Version.objects.filter(Q(current_version=True))
        cleaned_data = self.cleaned_data['current_version']
        active_version.append(cleaned_data) if cleaned_data else None
        # if cleaned_data:
        #     active_version.append(cleaned_data)
        if len(active_version) == 1 and version:
            raise forms.ValidationError('Вы можете установить только одну версию в качестве текущей')

        return cleaned_data

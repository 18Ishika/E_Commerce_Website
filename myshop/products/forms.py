from django import forms
from .models import Product

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['name', 'description', 'price', 'category', 'stock']

class MultiFileInput(forms.ClearableFileInput):
    allow_multiple_selected = True

class ProductImageForm(forms.Form):
    images = forms.ImageField(
        widget=MultiFileInput(attrs={'multiple': True}),
        required=False
    )
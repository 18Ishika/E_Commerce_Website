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
from django import forms
from .models import Review

class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['rating', 'review_text']
        widgets = {
            'rating': forms.NumberInput(attrs={'min': 1, 'max': 5}),
            'review_text': forms.Textarea(attrs={'rows': 4})
        }

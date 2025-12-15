from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User,BuyerProfile,SellerProfile
from django.core.validators import RegexValidator
phone_validator = RegexValidator(
    regex=r'^\+?\d{7,15}$',
    message="Enter a valid phone number (7-15 digits, optional leading +)."
)

pincode_validator = RegexValidator(
    regex=r'^\d{4,10}$',
    message="Enter a valid pincode (4-10 digits)."
)

gst_validator = RegexValidator(
    regex=r'^[0-9A-Z]{15}$',
    message="Enter a valid 15-character GST number (uppercase letters & digits)."
)
class BuyerSignUpForm(UserCreationForm):
    email=forms.EmailField(required=True)
    phone=forms.CharField(required=False,max_length=15)
    class Meta: #django told about how to save as per model
        model=User
        fields=("username","email","phone","password1","password2")
    def save(self,commit=True):
        user=super().save(commit=False)
        user.role='buyer'
        if commit:
            user.save()
        return user
class BuyerProfileForm(forms.ModelForm):
    #we can take everything thru meta field that takes default char field but some fields need extra validation so explicitly define them as they  override meta class
    pincode=forms.CharField(required=False,validators=[pincode_validator])
    class Meta:
        model=BuyerProfile
        fields=("default_address","city","state","pincode")

class SellerSignUpForm(UserCreationForm):
    email=forms.EmailField(required=True)
    phone=forms.CharField(required=False,max_length=15,validators=[phone_validator])
    class Meta:
        model = User
        fields = ("username", "email", "phone", "password1", "password2")

    def save(self, commit=True):
        user = super().save(commit=False)
        user.role = "seller"
        if commit:
            user.save()
        return user
class SellerProfileForm(forms.ModelForm):
    gst_number = forms.CharField(required=False, validators=[gst_validator])

    class Meta:
        model = SellerProfile
        fields = ("shop_name", "shop_description", "gst_number", "business_address")
        widgets = {
            "shop_description": forms.Textarea(attrs={"rows": 3}),
            "business_address": forms.Textarea(attrs={"rows": 3}),
        }
    
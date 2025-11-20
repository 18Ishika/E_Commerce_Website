# yourapp/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path("signup/buyer/", views.buyer_signup, name="buyer_signup"),
    path("signup/seller/", views.seller_signup, name="seller_signup"),
    path("login/",views.user_login,name='login'),

]

# yourapp/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path("signup/buyer/", views.buyer_signup, name="buyer_signup"),
    path("signup/seller/", views.seller_signup, name="seller_signup"),
    path("login/",views.user_login,name='login'),
    path("logout/",views.logoutUser,name='logout'),
    path("profile/", views.profile, name="profile"),
    path("manage_listings/", views.manage_listings, name="manage_listings"),
    path("seller_orders/", views.seller_orders, name="seller_orders"),
    
]

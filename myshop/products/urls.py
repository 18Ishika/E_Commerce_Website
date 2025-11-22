from django.urls import path
from . import views

urlpatterns = [
    path("", views.product_list, name="product_list"),
    path("<int:pk>/", views.product_detail, name="product_detail"),
    path("add_product/", views.add_product, name="add_product"),
]

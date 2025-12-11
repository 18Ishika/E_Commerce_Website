from django.urls import path
from . import views

urlpatterns = [
    path("", views.product_list, name="product_list"),
    path("<int:pk>/", views.product_detail, name="product_detail"),
    path("add_product/", views.add_product, name="add_product"),
    path('edit/<int:pk>/', views.edit_product, name='edit_product'),
    path('product/<int:product_id>/review/', views.add_review, name='add_review'),
    path("delete/<int:product_id>/", views.delete_product, name="delete_product"),


]

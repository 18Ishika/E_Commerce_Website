from django.urls import path
from . import views

urlpatterns = [
    path("checkout/", views.checkout, name="checkout"),

    path("mock/<str:payment_id>/", views.mock_payment, name="mock_payment"),

    path("success/<str:payment_id>/", views.payment_success, name="payment_success"),

    path("failed/<str:payment_id>/", views.payment_failed, name="payment_failed"),
    path("order-history/", views.order_history, name="order_history"),
    path("seller/orders/", views.seller_orders, name="seller_orders"),
    path("seller/order/<int:order_id>/update/", views.update_order_status, name="update_order_status"),
]

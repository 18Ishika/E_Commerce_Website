import uuid
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from django.db import transaction
from django.db.models import Prefetch

from .models import Payment, Order, OrderItem, OrderStatusHistory
from products.models import Product
from cart.models import Cart, CartProduct


@login_required
def checkout(request):
    """
    Handles both direct product purchase and cart checkout.
    Generates a new Payment object every time to prevent conflicts.
    """
    product_id = request.POST.get("product_id")

    if product_id:
        # Direct buy
        product = get_object_or_404(Product, id=product_id)
        quantity = int(request.POST.get("quantity", 1))
        total_amount = product.price * quantity

        payment = Payment.objects.create(
            payment_id=f"MOCKPAY-{uuid.uuid4().hex[:10].upper()}",
            amount=total_amount,
            status="PENDING"
        )

        order = Order.objects.create(
            user=request.user,
            payment=payment,
            total_amount=total_amount,
            current_status="PAYMENT_SUCCESS"
        )

        OrderItem.objects.create(
            order=order,
            product=product,
            product_name=product.name,
            quantity=quantity,
            price=product.price,
            total=total_amount
        )

    else:
        # Cart checkout
        cart = Cart.objects.filter(user=request.user, is_ordered=False).first()
        if not cart or cart.cart_products.count() == 0:
            return render(request, 'payment/failed.html', {'msg': 'Your cart is empty'})

        total_amount = cart.cart_total()
        payment = Payment.objects.create(
            payment_id=f"MOCKPAY-{uuid.uuid4().hex[:10].upper()}",
            amount=total_amount,
            status="PENDING"
        )

        order = Order.objects.create(
            user=request.user,
            payment=payment,
            total_amount=total_amount,
            current_status="PAYMENT_SUCCESS"
        )

        for item in cart.cart_products.all():
            OrderItem.objects.create(
                order=order,
                product=item.product,
                product_name=item.product.name,
                quantity=item.quantity,
                price=item.product_price,
                total=item.total_price()
            )

        cart.is_ordered = True
        cart.save()

    return redirect(reverse("mock_payment", args=[payment.payment_id]))


@login_required
def seller_orders(request):
    orders = (
        Order.objects
        .filter(items__product__seller=request.user)
        .distinct()
        .select_related("payment")
        .prefetch_related(
            Prefetch(
                "items",
                queryset=OrderItem.objects.filter(product__seller=request.user)
            )
        )
        .order_by("-created_at")
    )
    return render(request, "payment/seller_orders.html", {"orders": orders})


def mock_payment(request, payment_id):
    payment = get_object_or_404(Payment, payment_id=payment_id)
    return render(request, "payment/mock_payment.html", {"payment": payment})


@transaction.atomic
def payment_success(request, payment_id):
    payment = get_object_or_404(Payment, payment_id=payment_id)
    if payment.status != "PENDING":
        # Already processed
        return redirect('order_history')

    payment.status = "SUCCESS"
    payment.save()

    order = Order.objects.select_for_update().get(payment=payment)
    order.current_status = "PAYMENT_SUCCESS"
    order.save()

    # Update stock
    for item in order.items.select_related("product"):
        product = item.product
        if product.stock < item.quantity:
            order.current_status = "CANCELLED"
            order.save()
            payment.status = "FAILED"
            payment.save()

            OrderStatusHistory.objects.create(
                order=order,
                status="CANCELLED",
                note=f"Insufficient stock for {product.name}"
            )

            return render(request, "payment/failed.html", {"msg": f"Insufficient stock for {product.name}"})

        product.stock -= item.quantity
        product.save()

    # Record status history
    OrderStatusHistory.objects.create(
        order=order,
        status="PAYMENT_SUCCESS",
        note="Payment successful, stock updated"
    )

    return render(request, "payment/success.html", {"payment": payment})


def payment_failed(request, payment_id):
    payment = get_object_or_404(Payment, payment_id=payment_id)
    payment.status = "FAILED"
    payment.save()

    order = Order.objects.get(payment=payment)
    order.current_status = "CANCELLED"
    order.save()

    OrderStatusHistory.objects.create(
        order=order,
        status="CANCELLED",
        note="Payment failed"
    )

    return render(request, "payment/failed.html", {"payment": payment})


@login_required
def order_history(request):
    orders = (
        Order.objects
        .filter(user=request.user)
        .select_related("payment")
        .prefetch_related("items", "status_updates")
        .order_by("-created_at")
    )
    return render(request, "payment/order_history.html", {"orders": orders})


# ----------------------------------------------------------
# Seller updates shipment
# ----------------------------------------------------------
@login_required
def update_shipment_status(request, order_id):
    order = get_object_or_404(Order, id=order_id)

    if request.method == "POST":
        new_status = request.POST.get("tracking_status")
        tracking_id = request.POST.get("tracking_id")

        order.current_status = new_status
        if tracking_id:
            order.tracking_id = tracking_id
        order.save()

        OrderStatusHistory.objects.create(
            order=order,
            status=new_status,
            note=f"Shipment updated by seller. Tracking ID: {tracking_id or 'N/A'}"
        )

        return redirect("seller_orders")

    return render(request, "payment/seller_update_order.html", {"order": order})


@login_required
def update_order_status(request, order_id):
    order = get_object_or_404(Order, id=order_id)

    if order.payment.status != "SUCCESS":
        return redirect("seller_orders")

    if request.method == "POST":
        new_status = request.POST.get("status")
        note = request.POST.get("note", "")

        order.current_status = new_status
        order.save()

        OrderStatusHistory.objects.create(
            order=order,
            status=new_status,
            note=note
        )

        return redirect("seller_orders")

    return render(request, "payment/seller_update_order.html", {"order": order})

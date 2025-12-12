
# Create your views here.
import uuid
from django.shortcuts import render, redirect ,get_object_or_404
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from .models import Payment,Order,OrderItem
from products.models import Product
from cart.models import Cart, CartProduct


@login_required
def checkout(request):
    product_id=request.POST.get("product_id")
    if product_id:
        # Direct buy
        product = get_object_or_404(Product, id=product_id)
        quantity = int(request.POST.get("quantity", 1))
        total_amount = product.price * quantity

        payment_id = f"MOCKPAY-{uuid.uuid4().hex[:10].upper()}"
        payment = Payment.objects.create(payment_id=payment_id, amount=total_amount, status="PENDING")
        order = Order.objects.create(user=request.user, payment=payment, total_amount=total_amount)
        OrderItem.objects.create(
            order=order,
            product=product,
            product_name=product.name,
            quantity=quantity,
            price=product.price,
            total=total_amount
        )

    else:
        cart=Cart.objects.filter(user=request.user,is_ordered=False).first()
        if not cart or cart.cart_products.count()==0:
            return render(request,'payment/failed.html',{'msg':'Your cart is empty'})
        total_amount=cart.cart_total()
        payment_id=f"MOCKPAY-{uuid.uuid4().hex[:10].upper()}"
        payment = Payment.objects.create(
            payment_id=payment_id,
            amount=total_amount,
            status="PENDING"
        )
        order = Order.objects.create(
            user=request.user,
            payment=payment,
            total_amount=total_amount
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

        # Redirect to mock payment UI
    return redirect(reverse("mock_payment", args=[payment.payment_id]))
def mock_payment(request, payment_id):
    """Fake payment page with 'Pay' or 'Fail' buttons."""
    payment = get_object_or_404(Payment, payment_id=payment_id)
    return render(request, "payment/mock_payment.html", {"payment": payment})
def payment_success(request, payment_id):
    payment = get_object_or_404(Payment, payment_id=payment_id)
    payment.status = "SUCCESS"
    payment.save()
    order = Order.objects.get(payment=payment)
    order.status = "SUCCESS"
    order.save()
    return render(request, "payment/success.html", {"payment": payment})
def payment_failed(request, payment_id):
    payment = get_object_or_404(Payment, payment_id=payment_id)
    payment.status = "FAILED"
    payment.save()
    order = Order.objects.get(payment=payment)
    order.status = "FAILED"
    order.save()
    return render(request, "payment/failed.html", {"payment": payment})


@login_required
def order_history(request):
    orders = Order.objects.filter(user=request.user).order_by('-created_at')
    return render(request, "payment/order_history.html", {"orders": orders})

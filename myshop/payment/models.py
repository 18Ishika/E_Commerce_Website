from django.db import models  
from django.conf import settings
from products.models import Product


class Payment(models.Model):
    STATUS_CHOICES = [
        ("PENDING", "Pending"),
        ("SUCCESS", "Success"),
        ("FAILED", "Failed"),
    ]

    payment_id = models.CharField(max_length=50, unique=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(
        max_length=10,
        choices=STATUS_CHOICES,
        default="PENDING"
    )
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.payment_id} - {self.status}"


# ⭐ UPDATED ORDER MODEL WITH TRACKING
class Order(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )

    payment = models.OneToOneField(
        Payment,
        on_delete=models.CASCADE,
        related_name="order"
    )

    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)

    # 🔥 Primary tracking status for quick display
    current_status = models.CharField(
        max_length=30,
        default="PAYMENT_SUCCESS",
        choices=[
            ("PAYMENT_SUCCESS", "Payment Successful"),
            ("SHIPPED", "Shipped"),
            ("OUT_FOR_DELIVERY", "Out for Delivery"),
            ("DELIVERED", "Delivered"),
            ("CANCELLED", "Cancelled"),
        ]
    )

    # 🔥 Optional: tracking ID (like BlueDart / Delhivery / Speed Post)
    tracking_id = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        return f"Order #{self.id}"
    

# Order items remain same
class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name="items")
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    product_name = models.CharField(max_length=255)
    quantity = models.PositiveIntegerField(default=1)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    total = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.product_name} x {self.quantity}"


# ⭐ COMPLETE ORDER STATUS HISTORY MODEL
class OrderStatusHistory(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name="status_updates")

    status = models.CharField(
        max_length=30,
        choices=[
            ("PAYMENT_SUCCESS", "Payment Successful"),
            ("SHIPPED", "Shipped"),
            ("OUT_FOR_DELIVERY", "Out for Delivery"),
            ("DELIVERED", "Delivered"),
            ("CANCELLED", "Cancelled"),
        ]
    )

    note = models.TextField(blank=True, null=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Order {self.order.id} - {self.status}"

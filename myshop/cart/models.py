from django.db import models

# Create your models here.
from django.conf import settings
from products.models import Product

class Cart(models.Model):
    user=models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='carts'
    )
    is_ordered=models.BooleanField(default=False)
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)
    def cart_total(self):
        return sum(item.total_price() for item in self.cart_products.all())
    def __str__(self):
        return f"Cart ({self.user.username})"


class CartProduct(models.Model):
    cart=models.ForeignKey(
        Cart,
        on_delete=models.CASCADE,
        related_name="cart_products"
    )
    product=models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity=models.PositiveIntegerField(default=1)
    product_price=models.DecimalField(max_digits=10,decimal_places=2)

    def total_price(self):
        return self.product_price*self.quantity
    def __str__(self):
        return f"{self.product.name}X{self.quantity}"
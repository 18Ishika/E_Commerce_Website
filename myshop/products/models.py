from django.db import models
from django.conf import settings
class Category(models.Model):
    name=models.CharField(max_length=255)
    parent=models.ForeignKey(
        "self",
        on_delete=models.PROTECT,
        blank=True,
        null=True,
        related_name="subcategories"
    )

    class Meta:
        verbose_name_plural="Categories"
        #(e.g., if your model is Category, it might display "Categorys" or "Categories" in the admin).--bydefault so to keep it gramaatically coreect
    def __str__(self):
        if self.parent:
            return f"{self.parent}->{self.name}"
        return self.name

class Product(models.Model):
    seller=models.ForeignKey(
        settings.AUTH_USER_MODEL,

        on_delete=models.CASCADE,
        limit_choices_to={'role':'seller'}

    )
    name=models.CharField(max_length=255)
    description=models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,     # keep product even if category deleted
        null=True
    )
    average_rating = models.FloatField(default=0)
    total_reviews = models.PositiveIntegerField(default=0)
    stock = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.name} - {self.seller.username}"
class ProductImage(models.Model):
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name="images"
    )
    image = models.ImageField(upload_to="product_images/")

    def __str__(self):
        return f"Image for {self.product.name}"
class Review(models.Model):
    RATING_CHOICES = [(i, i) for i in range(1, 6)]  # 1–5 stars

    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="reviews")
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    rating = models.PositiveSmallIntegerField(choices=RATING_CHOICES)
    review_text = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("product", "user")   # prevent multiple reviews per user

    def __str__(self):
        return f"{self.product.name} - {self.rating}★ by {self.user.username}"

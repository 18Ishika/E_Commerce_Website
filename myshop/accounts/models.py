from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
class User(AbstractUser):
    ROLE_CHOICES=(
        ('buyer','Buyer'),
        ('seller','Seller')
    )
    role=models.CharField(max_length=10,choices=ROLE_CHOICES)
    phone=models.CharField(max_length=15,blank=True,null=True)
    def __str__(self):
        return f"{self.username}({self.role})"


#Buyer profile
class BuyerProfile(models.Model):
    user=models.OneToOneField(User,on_delete=models.CASCADE,related_name="buyer_profile")
    default_address=models.TextField(blank=True,null=True)
    city = models.CharField(max_length=100, blank=True, null=True)
    state = models.CharField(max_length=100, blank=True, null=True)
    pincode = models.CharField(max_length=10, blank=True, null=True)

    def __str__(self):
        return f"BuyerProfile - {self.user.username}"  #how it displays on admin page -- john(seller)
    
class SellerProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='seller_profile')
    shop_name = models.CharField(max_length=255)
    shop_description = models.TextField(blank=True, null=True)
    gst_number = models.CharField(max_length=20, blank=True, null=True)
    business_address = models.TextField(blank=True, null=True)
    rating = models.FloatField(default=0)

    def __str__(self):
        return f"SellerProfile - {self.shop_name}"

# @receiver(post_save,sender=User)  #triggers whenever a user is created no need to manually save it
# def create_user_profiles(sender,instance,created,**kwargs):
#     if created:
#         if instance.role=='buyer':
#             BuyerProfile.objects.create(user=instance)
#         elif instance.role=='seller':
#             SellerProfile.objects.create(user=instance)
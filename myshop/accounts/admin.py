from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, BuyerProfile, SellerProfile


class CustomUserAdmin(UserAdmin):
    model = User

    # What fields to show in the user list
    list_display = ("username", "email", "role", "phone", "is_staff", "is_active")
    list_filter = ("role", "is_staff", "is_active")

    # These fields appear in the user edit page
    fieldsets = (
        (None, {"fields": ("username", "password")}),
        ("Personal Info", {"fields": ("first_name", "last_name", "email", "phone", "role")}),
        ("Permissions", {"fields": ("is_active", "is_staff", "is_superuser", "groups", "user_permissions")}),
        ("Important dates", {"fields": ("last_login", "date_joined")}),
    )

    # Fields shown when creating a user in admin
    add_fieldsets = (
        (None, {
            "classes": ("wide",),
            "fields": ("username", "email", "role", "phone", "password1", "password2"),
        }),
    )


admin.site.register(User, CustomUserAdmin)
admin.site.register(BuyerProfile)
admin.site.register(SellerProfile)
  
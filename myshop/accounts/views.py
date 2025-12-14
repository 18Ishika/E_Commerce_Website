# yourapp/views.py
from django.shortcuts import render, redirect,get_object_or_404
from django.contrib.auth import login,authenticate , logout
from django.db import transaction
from django.contrib import messages
from products.views import product_list
from django.contrib.auth.decorators import login_required
from payment.models import Order

from .forms import (
    BuyerSignUpForm, BuyerProfileForm,
    SellerSignUpForm, SellerProfileForm,
)

def buyer_signup(request):
    if request.method == "POST":
        user_form = BuyerSignUpForm(request.POST)
        profile_form = BuyerProfileForm(request.POST)
        if user_form.is_valid() and profile_form.is_valid():
            with transaction.atomic():
                user = user_form.save()  # sets role='buyer'
                profile = profile_form.save(commit=False)
                profile.user = user
                profile.save()
            login(request, user)
            return redirect("product_list")  # change to your home route name
    else:
        user_form = BuyerSignUpForm()
        profile_form = BuyerProfileForm()
    return render(request, "signup/buyer_signup.html", {"user_form": user_form, "profile_form": profile_form})

def seller_signup(request):
    if request.method == "POST":
        user_form = SellerSignUpForm(request.POST)
        profile_form = SellerProfileForm(request.POST)
        if user_form.is_valid() and profile_form.is_valid():
            with transaction.atomic():
                user = user_form.save()  # sets role='seller'
                profile = profile_form.save(commit=False)
                profile.user = user
                profile.save()
            login(request, user)
            return redirect("product_list")  # change to your seller dashboard route
    else:
        user_form = SellerSignUpForm()
        profile_form = SellerProfileForm()
    return render(request, "signup/seller_signup.html", {"user_form": user_form, "profile_form": profile_form})


def user_login(request):
    if request.method=='POST':
        username=request.POST.get("username")
        password=request.POST.get("password")
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request,user)
            if user.role=='buyer':
                return redirect("product_list")  
            elif user.role=='seller':
                return redirect("product_list")
            else:
                return redirect("product_list")
        else:
            messages.error(request,"Invalid username or password")
    return render(request, "login.html")

def logoutUser(request):
    logout(request)
    return redirect("product_list")

@login_required
def profile(request):
    user=request.user
    if user.is_superuser:
        return redirect('/admin/')
    elif user.role=='buyer':
        profile=getattr(user, "buyer_profile", None)
    elif user.role=='seller':
        profile=getattr(user, "seller_profile", None)
    
    context = {
        "user": user,
        "profile": profile
    }
    return render(request,'profile.html',context)
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from products.models import Product
from django.core.paginator import Paginator

@login_required
def manage_listings(request):

    # Ensure only sellers can access this page
    if request.user.role != "seller":
        messages.error(request, "Only sellers can manage listings.")
        return redirect("product_list")

    # Fetch ONLY the products listed by this seller
    seller_products = Product.objects.filter(seller=request.user).order_by("-created_at")

    # Optional: Pagination → 10 items per page
    paginator = Paginator(seller_products, 10)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    return render(request, "manage_listings.html", {
        "page_obj": page_obj,
    })

@login_required
def seller_orders(request):
    
    seller_products = Product.objects.filter(seller=request.user)
    orders = Order.objects.filter(
        items__product__in=seller_products
    ).distinct().order_by('-created_at')

    return render(request, "payment/seller_orders.html", {
        "orders": orders
    })
@login_required
def edit_profile(request):
    user = request.user

    if request.method == "POST":
        # Update User fields
        user.username = request.POST.get("username", user.username)
        user.email = request.POST.get("email", user.email)
        user.phone = request.POST.get("phone", user.phone)
        user.save()

        if user.role == "buyer":
            profile = user.buyer_profile
            profile.default_address = request.POST.get("default_address", profile.default_address)
            profile.city = request.POST.get("city", profile.city)
            profile.state = request.POST.get("state", profile.state)
            profile.pincode = request.POST.get("pincode", profile.pincode)
            profile.save()
        elif user.role == "seller":
            profile = user.seller_profile
            profile.shop_name = request.POST.get("shop_name", profile.shop_name)
            profile.shop_description = request.POST.get("shop_description", profile.shop_description)
            profile.gst_number = request.POST.get("gst_number", profile.gst_number)
            profile.business_address = request.POST.get("business_address", profile.business_address)
            # Note: rating is not editable by seller
            profile.save()

        messages.success(request, "Profile updated successfully!")
        return redirect("edit_profile")

    context = {
        "user": user,
    }
    return render(request, "edit_profile.html", context)
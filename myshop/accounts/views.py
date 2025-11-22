# yourapp/views.py
from django.shortcuts import render, redirect
from django.contrib.auth import login,authenticate , logout
from django.db import transaction
from django.contrib import messages
from products.views import product_list
from django.contrib.auth.decorators import login_required

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
    if user.role=='buyer':
        profile=user.buyerprofile
    else:
        profile=user.sellerprofile
    return render(request,'profile.html',{"user":user,'profile':profile})
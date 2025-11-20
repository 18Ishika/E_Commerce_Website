# yourapp/views.py
from django.shortcuts import render, redirect
from django.contrib.auth import login,authenticate
from django.db import transaction
from django.contrib import messages
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
            return redirect("home")  # change to your home route name
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
            return redirect("home")  # change to your seller dashboard route
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
                return render(request,'dashboard.html')
            elif user.role=='seller':
                return render(request,'dashboard.html')
            else:
                return redirect("home")
        else:
            messages.error(request,"Invalid username or password")
    return render(request, "login.html")
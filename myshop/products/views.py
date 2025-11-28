from django.shortcuts import render,get_object_or_404,redirect
from .forms import ProductForm,ProductImageForm
from .models import Product, ProductImage
from django.contrib import messages
from django.contrib.auth.decorators import login_required
# Create your views here.

from .models import Product

def product_list(request):
    products = Product.objects.all().order_by('-created_at')
    return render(request, 'products/product_list.html', {'products': products})

def product_detail(request, pk):
    product = get_object_or_404(Product, pk=pk)
    return render(request, 'products/product_detail.html', {'product': product})

from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .forms import ProductForm, ProductImageForm
from .models import ProductImage

@login_required
def add_product(request):
    if request.user.role != "seller":   # to prevent buyers adding products
        return redirect("product_list")

    if request.method == "POST":
        form = ProductForm(request.POST)
        image_form = ProductImageForm(request.POST, request.FILES)

        if form.is_valid():
            product = form.save(commit=False)
            product.seller = request.user
            product.save()

            # Save multiple images
            images = request.FILES.getlist("images")
            for img in images:
                ProductImage.objects.create(product=product, image=img)

            return redirect("product_list")   # after successful product upload

    else:
        form = ProductForm()
        image_form = ProductImageForm()

    return render(request, "products/add_product.html", {
        "form": form,
        "image_form": image_form
    })

@login_required
def edit_product(request, pk):
    product = get_object_or_404(Product, id=pk)

    if product.seller != request.user:
        messages.error(request, "You are not allowed to edit this product.")
        return redirect("product_detail", pk=pk)

    if request.method == "POST":
        form = ProductForm(request.POST, instance=product)
        img_form = ProductImageForm(request.POST, request.FILES)

        if form.is_valid():
            form.save()

            # Handle multiple images
            if request.FILES.getlist('images'):
                for file in request.FILES.getlist('images'):
                    ProductImage.objects.create(product=product, image=file)

            messages.success(request, "Product updated successfully.")
            return redirect("product_detail", pk=pk)

    else:
        form = ProductForm(instance=product)
        img_form = ProductImageForm()

    return render(request, "products/edit_product.html", {
        "form": form,
        "img_form": img_form,
        "product": product
    })
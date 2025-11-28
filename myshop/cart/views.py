from django.shortcuts import render,get_object_or_404,redirect
from django.contrib.auth.decorators import login_required
# Create your views here.
from .models import Cart, CartProduct
from products.models import Product
from django.contrib import messages
from django.contrib.auth.decorators import login_required

def get_user_cart(user):
    cart,created=Cart.objects.get_or_create(user=user,is_ordered=False)
    return cart

def add_product_to_cart(user,product_id,qty=1):
    product=get_object_or_404(Product,id=product_id)
    if product.stock<qty:
        return None , 'Not enough stock available'
    cart=get_user_cart(user)
    cart_item,created=CartProduct.objects.get_or_create(
        cart=cart,
        product=product,
        defaults={
            "product_price":product.price,
            "quantity":qty
        }
    )
    if not created:
        if product.stock<cart_item.quantity+qty:
            return None , "Not enough stock to increase quantity"
        cart_item.quantity+=qty
        cart_item.save()
    return cart , None

#Main views
@login_required
def cart_view(request):
    cart=get_user_cart(request.user)
    items=cart.cart_products.all()
    context={
        "cart":cart,
        "items":items,
        "cart_total":cart.cart_total(),
    }
    return render(request,"cart/cart_view.html",context)
@login_required
def add_to_cart_view(request,product_id):
    cart,error=add_product_to_cart(request.user,product_id)
    if error:
        messages.error(request,error)
    else:
        messages.success(request,"Product added to cart")
    return redirect("cart_view")


@login_required
def remove_from_cart(request,item_id):
    item=get_object_or_404(CartProduct,id=item_id,cart__user=request.user)
    item.delete()
    messages.info(request,"Item removed from the cart")
    return redirect("cart_view")


@login_required
def increase_qty(request,item_id):
    item=get_object_or_404(CartProduct,id=item_id,cart__user=request.user)
    if item.product.stock<=item.quantity:
        messages.error(request,"Cannot exceed available stock")
        return redirect("cart_view")
    item.quantity+=1
    item.save()
    return redirect("cart_view")

@login_required
def decrease_qty(request,item_id):
    item=get_object_or_404(CartProduct,id=item_id,cart__user=request.user)
    if item.quantity>1:
        item.quantity-=1
        item.save()
    else:
        item.delete()
    return redirect("cart_view")

@login_required
def clear_cart(request):
    cart=get_user_cart(request.user)
    cart.cart_products.all().delete()
    messages.warning(request,"Your cart has been cleared.")
    return redirect("cart_view")
   
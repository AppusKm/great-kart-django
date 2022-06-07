from django.http import HttpResponse
from store.models import Product, Variations
from django.shortcuts import get_object_or_404, redirect, render
from .models import Cart, CartItems

from django.db import connection
from django.core.exceptions import ObjectDoesNotExist
# Create your views here.

def _cartId(request):
    ses_id = request.session.session_key
    if not ses_id:
        ses_id = request.session.create()
    return ses_id
def addToCart(request,id):
    product = Product.objects.get(id = id)
    product_variations = []
    if request.method == 'POST':
        for item in request.POST:
            key = item
            value = request.POST[key]
            try:
                variations = Variations.objects.get(product = product,variation_category__iexact=key,variation_value__iexact=value)
                product_variations.append(variations)
                # return HttpResponse((connection.queries))
                # exit()
                print(variations)
            except:
                pass
        # color = request.POST['color']
        # size = request.POST['size']
    # return HttpResponse(color+' '+size)
    # exit()
    try:
        cart = Cart.objects.get(cart_id = _cartId(request))
    except Cart.DoesNotExist:
        cart = Cart.objects.create(
            cart_id = _cartId(request),
        )
        cart.save()
    is_cart_item_exist = CartItems.objects.filter(product = product,cart = cart).exists()
   
    if is_cart_item_exist:
        cart_item = CartItems.objects.filter(product = product,cart = cart)
        # existing variations ->database
        # current variations -> product_variation_id
        # item id ->database
        ex_var_list = []
        id = []
        for item in cart_item:
                existing_variations = item.variations.all()
                ex_var_list.append(list(existing_variations))
                id.append(item.id)

        # print('CURRENT',ex_var_list)
        if product_variations in ex_var_list:
            index = ex_var_list.index(product_variations)
            item_id = id[index]
            item = CartItems.objects.get(product = product,id = item_id)
            item.quantity += 1
            item.save()
            # return HttpResponse(item_id)
        else:
         item = CartItems.objects.create(product = product,cart = cart, quantity = 1)
         if len(product_variations)  > 0:
            item.variations.clear()
            item.variations.add(*product_variations)
        item.save()
        # cart_item.quantity += 1 
            # cart_item.save()
    # except CartItems.DoesNotExist:
    else:
        cart_items = CartItems.objects.create(
            product = product,
            cart = cart,
            quantity = 1
        )
        if len(product_variations)  > 0:
            cart_items.variations.clear()
            cart_items.variations.add(*product_variations)
        cart_items.save()
    return redirect('cart')


def cart(request,total=0,quantity=0,cart_items = None):
    tax = 0
    grand_total = 0
    try:
        cart = Cart.objects.get(cart_id = _cartId(request))
        # print(connection.queries)
        cart_items = CartItems.objects.filter(cart = cart,is_active = True)
        
        for items in cart_items:
            total += (items.product.price * items.quantity) 
            quantity += items.quantity
        tax = (2*total) / 100
        grand_total = total + tax

    # except Exception as e:
    #     print(e)
    except ObjectDoesNotExist:
        pass
    context = {
        'total':total,
        'quantity':quantity,
        'cart_items':cart_items,
        'tax':tax,
        'grand_total':grand_total,
    }
    # return HttpResponse('cart_items')
    return render(request,'cart/cart.html',context)

def removeCart(request,product_id,cart_item_id):
    cart = Cart.objects.get(cart_id = _cartId(request))
    product = get_object_or_404(Product,id = product_id)
    try:
        cart_items = CartItems.objects.get(product = product,cart = cart,id = cart_item_id)
        if cart_items.quantity > 1:
            cart_items.quantity -= 1
            cart_items.save()
        else:
            cart_items.delete()
    except:
        pass
    
    return redirect('cart')

def removeCartItem(request,product_id,cart_item_id):
    cart = Cart.objects.get(cart_id = _cartId(request))
    product = get_object_or_404(Product,id = product_id)
    # return HttpResponse(connection.queries)
    cart_items = CartItems.objects.get(product = product,cart = cart,id = cart_item_id)
    cart_items.delete()
    return redirect('cart')

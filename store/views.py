
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, render
from cart.models import CartItems
from store.models import Product
from category.models import Category
from django.db import connection
from cart.views import _cartId
from django.core.paginator import EmptyPage,PageNotAnInteger,Paginator
from django.db.models import Q
# Create your views here.
def store(request,category_slug = None):
    categories = None
    products = None
    if category_slug:
        categories = get_object_or_404(Category,slug = category_slug)
        # print(categories.id)
        # print(categories)
        # print(categories.query)
        # print(connection.queries)
        products = Product.objects.all().filter(category = categories, is_available = True).order_by('id')
        # products = Product.objects.all().filter(category_id = categories.id, is_available = True)
        paginator = Paginator(products,6)
        page = request.GET.get('page')
        paged_products = paginator.get_page(page)
        product_count =products.count()
    else:
        products = Product.objects.all().filter(is_available = True).order_by('id')
        paginator = Paginator(products,6)
        page = request.GET.get('page')
        paged_products = paginator.get_page(page)
        product_count =products.count()
        category_slug = ''
    context = {
        'products':paged_products,
        'product_count':product_count,
        'slg':category_slug,
        }
    return render(request,'store/store.html',context)

    # to list all category we using a python function called context processor
def productDetail(request,category_slug = None,product_slug = None):
    try:
        single_product = Product.objects.get(category__slug = category_slug,slug = product_slug)
        # print(connection.queries)
        in_cart = CartItems.objects.filter(cart__cart_id = _cartId(request),product = single_product).exists()
       
        # return HttpResponse(connection.queries)
        # return HttpResponse(in_cart)
        # exit()
    except Exception as e :
        raise e
    context = {
        'single_product':single_product,
        'product_count':'',
        'slg':'',
        'in_cart':in_cart,
        }
    return render(request,'store/product_detail.html',context)


def search(request):
    if 'keyword' in request.GET:
        keyword = request.GET['keyword']
        if keyword:
            products = Product.objects.order_by('-created_date').filter(Q(description__icontains=keyword) | Q(product_name__icontains=keyword))
            product_count =products.count()
    context = {
        'products':products,
        'product_count':product_count,
        'keyword':keyword,
        'slg':keyword,
        }
    return render(request,'store/store.html',context)
    # return HttpResponse('search page')
    # exit()

    

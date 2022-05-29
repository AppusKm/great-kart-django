
from django.shortcuts import get_object_or_404, render
from store.models import Product
from category.models import Category
from django.db import connection
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
        products = Product.objects.all().filter(category = categories, is_available = True)
        # products = Product.objects.all().filter(category_id = categories.id, is_available = True)
        product_count =products.count()
    else:
        products = Product.objects.all().filter(is_available = True)
        product_count =products.count()
        category_slug = ''
    context = {
        'products':products,
        'product_count':product_count,
        'slg':category_slug,
        }
    return render(request,'store/store.html',context)

    # to list all category we using a python function called context processor
def productDetail(request,category_slug = None,product_slug = None):
    try:
        single_product = Product.objects.get(category__slug = category_slug,slug = product_slug)
        print(connection.queries)
    except Exception as e :
        raise e
    context = {
        'single_product':single_product,
        'product_count':'',
        'slg':'',
        }
    return render(request,'store/product_detail.html',context)
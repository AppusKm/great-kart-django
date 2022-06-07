
from . import views
from django.urls import path


urlpatterns = [
    path('', views.store,name='store'),
    path('product/<slug:category_slug>/', views.store,name='products_by_category'),
    path('product/<slug:category_slug>/<slug:product_slug>/', views.productDetail,name='products_detail'),
    path('search/',views.search,name='search'),
]
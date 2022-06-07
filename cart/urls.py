from django.urls import path
from . import views
urlpatterns = [
    path('',views.cart,name='cart'),
    path('add_cart/<int:id>/',views.addToCart,name='add_cart'),
    path('remove_cart/<int:product_id>/<int:cart_item_id>',views.removeCart,name='remove_cart'),
    path('remove_cart_item/<int:product_id>/<int:cart_item_id>',views.removeCartItem,name='remove_cart_item'),
]
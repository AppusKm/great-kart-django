from django.db import models
from store.models import Product,Variations
# Create your models here.
class Cart(models.Model):
    cart_id = models.CharField(max_length=200,blank = True)
    date_added = models.DateField(auto_now_add=True)

    def __str__(self) -> str:
        return self.cart_id

class CartItems(models.Model):
    product = models.ForeignKey(Product,on_delete=models.CASCADE)
    variations = models.ManyToManyField(Variations,blank=True)
    cart = models.ForeignKey(Cart,on_delete=models.CASCADE)
    quantity = models.IntegerField()
    is_active = models.BooleanField(default=True)

    def __unicode__(self) -> str:
        return self.product

    def sub_total(self):
        return self.product.price * self.quantity
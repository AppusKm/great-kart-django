from django.db import models
from django.urls import reverse

from category.models import Category

# Create your models here.
class Product(models.Model):
    product_name = models.CharField(max_length=200,unique=True)
    slug = models.SlugField(max_length=200,unique=True)
    description = models.TextField(max_length=500,blank=True)
    price = models.DecimalField(max_digits=20, decimal_places=2, default=0.0)
    image = models.ImageField(upload_to='photos/products',blank = True)
    stock = models.IntegerField()
    is_available = models.BooleanField(default=True)
    category = models.ForeignKey(Category,on_delete=models.SET_NULL,null=True)
    created_date = models.DateTimeField(auto_now_add=True)
    modified_date = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return super().__str__()
    def getProductUrl(self):
        return reverse('products_detail',args=[self.category.slug,self.slug]) #this will bring url of particular category
        

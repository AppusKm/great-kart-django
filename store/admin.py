from django.contrib import admin
from .models import Product,Variations
# Register your models here.

class ProductAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug':('product_name',)}
    list_display = ('product_name','slug','description','price','image','stock','is_available','category','created_date','modified_date')

class VariationsAdmin(admin.ModelAdmin):
   list_display = ('product','variation_category','variation_value','is_active','created_at')
   list_editable = ('is_active','variation_category','variation_value',)
   list_filter = ('product','variation_category','variation_value','created_at',)

admin.site.register(Product,ProductAdmin)
admin.site.register(Variations,VariationsAdmin)

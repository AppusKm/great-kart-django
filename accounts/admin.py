from django.contrib import admin
from .models import Account
from django.contrib.auth.admin import UserAdmin

# Register your models here.
class AccountAdmin(UserAdmin):
    list_display = ('first_name','last_name','user_name','phone_number','last_login','is_admin','is_staff','is_active','email','is_superadmin','date_joined')

    list_display_links = ('email','user_name')
    # search_fields = ()
    readonly_fields = ('last_login','date_joined')

    filter_horizontal = ()
    list_filter = ()
    fieldsets = ()
    ordering = ('-date_joined',)

admin.site.register(Account,AccountAdmin)
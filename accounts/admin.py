from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUser
from django.utils.translation import gettext as _

from . import models

# Register your models here.
class UserAdmin(BaseUser):
    ordering = ['id']
    list_display=   ['id', 'username', 'email', 'name']
    list_display_links=['id','email']
    fieldsets= (
        (None, {'fields': ('username', 'email','password',)}),
        (_('Personal info'), {'fields': ('name',)}),
        (_('Permissions'), {'fields': ('is_active', 'is_staff', 'is_superuser',)}),
        (_('Imp dates'), {'fields': ('last_login',)})   
    )
    add_fieldsets= (
        (None, {
            'class': ('wide'),
            'fields': ('name', 'email', 'password1','password2',)
        }),
    )
    
admin.site.register(models.User,UserAdmin)
admin.site.register(models.Profile)
from django.contrib import admin

# Register your models here.
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser, Roles

class CustomUserAdmin(UserAdmin):
    model = CustomUser
    fieldsets = UserAdmin.fieldsets + (
        ("Custom Fields", {'fields': ('phone_number', 'kyc_completed')}),
    )

admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(Roles)
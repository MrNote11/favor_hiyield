from django.contrib import admin
from .models import Customeruser



class CustomerUserAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'phone_no', 'is_admin', 'date_joined')
    search_fields = ('username', 'email')
    list_filter = ('is_admin', 'date_joined')

    def has_add_permission(self, request):
        return True  # Disable adding new users from admin

    def has_delete_permission(self, request, obj=None):
        return False  # Disable deleting users from admin
admin.site.register(Customeruser, CustomerUserAdmin)

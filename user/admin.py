from django.contrib import admin
from django_tenants.admin import TenantAdminMixin

from user.models import Client, CustomUser, Domain


@admin.register(Client)
class ClientAdmin(TenantAdminMixin, admin.ModelAdmin):
    list_display = ('name',)


@admin.register(CustomUser)
class CustomUserAdmin(admin.ModelAdmin):
    list_display = [
        "username", "email", "first_name", "last_name",
        "mobile_number",
        "is_mobile_verified",
        "business_name",
    ]


@admin.register(Domain)
class DomainAdmin(admin.ModelAdmin):
    list_display = ['domain', 'tenant']

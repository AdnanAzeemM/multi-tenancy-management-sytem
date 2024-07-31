from django.db import models
from django.contrib.auth.models import AbstractUser
from django.db.models.signals import post_save
from django.dispatch import receiver
from django_tenants.models import TenantMixin, DomainMixin
from django_tenants.utils import schema_context

from Ecommerce_tenant import settings


class Client(TenantMixin):
    name = models.CharField(max_length=100)
    created_on = models.DateField(auto_now_add=True)

    auto_create_schema = True


class Domain(DomainMixin):
    pass


class CustomUser(AbstractUser):
    mobile_number = models.CharField(max_length=20, null=True, blank=True)
    is_mobile_verified = models.BooleanField(default=False)
    password = models.CharField(max_length=255, )
    business_name = models.CharField(max_length=255, null=True, blank=True)

    def __str__(self):
        return self.username

    def get_domain(self):
        if self.business_name:
            business_name = self.business_name.strip().lower()
            try:
                domain = Domain.objects.get(tenant__schema_name=business_name)
                return domain.domain
            except Domain.DoesNotExist:
                return None
        return None


class Employee(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='employees')
    first_name = models.CharField(max_length=150, blank=True)
    last_name = models.CharField(max_length=150, blank=True)
    email = models.EmailField(blank=True)
    job_title = models.CharField(max_length=255, null=True, blank=True)
    department = models.CharField(max_length=255, null=True, blank=True)
    mobile_number = models.CharField(max_length=20, null=True, blank=True)
    is_mobile_verified = models.BooleanField(default=False)
    password = models.CharField(max_length=255, )

    def __str__(self):
        return f"{self.first_name} - {self.last_name}"


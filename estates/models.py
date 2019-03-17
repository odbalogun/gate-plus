from django.db import models
from tenant_schemas.models import TenantMixin
from .managers import EstateManager


# Create your models here.
class Estate(TenantMixin):
    name = models.CharField(max_length=100)
    slug = models.CharField(max_length=20)
    is_active = models.BooleanField(default=True)
    created_on = models.DateField(auto_now_add=True)

    auto_create_schema = True

    objects = models.Manager()
    tenancy = EstateManager()

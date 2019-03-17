from django.db import models
from django.conf import settings


class EstateManager(models.Manager):
    # def get_query_set(self):
    #     return super(EstateManager, self).get_query_set().filter(active=True)

    def create_estate(self, name, slug, **extra_fields):
        """
        Creates and saves an estate. Creates a new record in our multi-tenant system
        """
        tenant = self.model(domain_url="{}.{}".format(slug, settings.BASE_APP_URL), schema_name=slug, name=name)
        tenant.save(using=self._db)
        return tenant

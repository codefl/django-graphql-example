from django.db import models


class ProductModel(models.Model):
    name = models.CharField(max_length=32, blank=False)
    description = models.CharField(max_length=100, blank=True)
    sku_no = models.CharField(max_length=100, blank=False)

    def __str__(self):
        return self.name

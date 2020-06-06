from django.db import models
from mptt.models import MPTTModel, TreeForeignKey
from . import Currency


class CategoryModel(MPTTModel):
    name = models.CharField(max_length=100, blank=False)
    parent = TreeForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='children')

    class MPTTMeta:
        order_insertion_by = ['name']

    def __str__(self):
        return self.name


class ProductModel(models.Model):
    name = models.CharField(max_length=100, blank=False)
    description = models.CharField(max_length=100, blank=True)

    category = models.ForeignKey(CategoryModel, on_delete=models.DO_NOTHING, related_name='products',
                                 null=False, blank=False)

    def __str__(self):
        return self.name


class ProductVariationModel(models.Model):
    product = models.ForeignKey(ProductModel, on_delete=models.DO_NOTHING, related_name='variations',
                                null=False, blank=False)
    sku_no = models.CharField(max_length=100, blank=False)
    variation = models.CharField(max_length=100, blank=False)
    description = models.CharField(max_length=100, blank=True)

    currency = models.CharField(max_length=8, blank=False, choices=Currency.choices())
    price = models.IntegerField(null=False)

    def __str__(self):
        return self.variation

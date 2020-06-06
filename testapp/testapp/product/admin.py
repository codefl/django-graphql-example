from django.contrib import admin
from .models import ProductModel, ProductVariationModel, CategoryModel


admin.site.register(ProductModel)
admin.site.register(ProductVariationModel)
admin.site.register(CategoryModel)

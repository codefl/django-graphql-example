from django.contrib import admin
from .models import ProductModel, ProductVariationModel, CategoryModel


class ProductVariationModelInline(admin.TabularInline):
    model = ProductVariationModel
    extra = 1


class ProductModelAdmin(admin.ModelAdmin):
    fields = ['name', 'description', 'category']
    list_filter = ['category']
    search_fields = ['name']

    inlines = [ProductVariationModelInline]


admin.site.register(ProductModel, ProductModelAdmin)
admin.site.register(CategoryModel)

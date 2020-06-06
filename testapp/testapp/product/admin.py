from django.contrib import admin
from .models import ProductModel, ProductVariationModel, CategoryModel, TagModel


class ProductTagInline(admin.TabularInline):
    model = ProductModel.tags.through
    extra = 1


class ProductVariationModelInline(admin.TabularInline):
    model = ProductVariationModel
    extra = 1


class ProductModelAdmin(admin.ModelAdmin):
    fields = ['name', 'description', 'category']
    list_filter = ['category']
    search_fields = ['name']

    inlines = [ProductVariationModelInline, ProductTagInline]


admin.site.register(ProductModel, ProductModelAdmin)
admin.site.register(CategoryModel)
admin.site.register(TagModel)

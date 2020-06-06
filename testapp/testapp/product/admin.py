from django.contrib import admin
from .models import ProductModel, ProductVariationModel, CategoryModel, TagModel


#########################################################
# Many to many inline edit UI
#########################################################

class ProductTagInline(admin.TabularInline):
    model = ProductModel.tags.through
    extra = 1


#########################################################
# 1 to many inline edit UI
#########################################################

class ProductVariationModelInline(admin.TabularInline):
    model = ProductVariationModel
    extra = 1


#########################################################
# Define admin model for product (main object)
#########################################################

class ProductModelAdmin(admin.ModelAdmin):
    fields = ['name', 'description', 'category']
    list_filter = ['category']
    search_fields = ['name']

    inlines = [ProductVariationModelInline, ProductTagInline]


#########################################################
# Register the 1st level admin models
#########################################################

admin.site.register(ProductModel, ProductModelAdmin)
admin.site.register(CategoryModel)
admin.site.register(TagModel)

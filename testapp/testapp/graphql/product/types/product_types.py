import graphene
from graphene_django import DjangoObjectType
from ....product.models import ProductModel, CategoryModel, ProductVariationModel


###########################################################################
# Types
###########################################################################

class ProductType(DjangoObjectType):
    class Meta:
        model = ProductModel

    @staticmethod
    def resolve_category(root, info, **kwargs):
        return info.context.categories_by_category_id_loader.load(root.category_id)

    @staticmethod
    def resolve_variations(root, info, **kwargs):
        return info.context.variations_by_product_id_loader.load(root.id)


class CategoryType(DjangoObjectType):
    class Meta:
        model = CategoryModel

    @staticmethod
    def resolve_products(root, info, **kwargs):
        return info.context.products_by_category_id_loader.load(root.id)


class ProductVariationType(DjangoObjectType):
    class Meta:
        model = ProductVariationModel

    @staticmethod
    def resolve_product(root, info, **kwargs):
        return info.context.products_by_product_id_loader.load(root.product_id)

import graphene
from graphene_django import DjangoObjectType
from ....product.models import ProductModel, CategoryModel, ProductVariationModel
from ..dataloaders.product_dataloaders import CategoryLoader


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


class ProductVariationType(DjangoObjectType):
    class Meta:
        model = ProductVariationModel


class ErrorType(graphene.ObjectType):
    error_code = graphene.String()
    error_message = graphene.String()


class ProductResponseType(graphene.Union):
    class Meta:
        types = (ProductType, ErrorType)


class CategoryResponseType(graphene.Union):
    class Meta:
        types = (CategoryType, ErrorType)


class ProductVariationResponseType(graphene.Union):
    class Meta:
        types = (ProductVariationType, ErrorType)


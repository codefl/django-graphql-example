import graphene
from graphene_django import DjangoObjectType
from ....product.models import ProductModel, CategoryModel, ProductVariationModel


###########################################################################
# Types
###########################################################################

class ProductType(DjangoObjectType):
    class Meta:
        model = ProductModel


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


import graphene
from .product_types import ProductType, CategoryType, ProductVariationType
from ...common.common_types import ErrorType


class ProductResponseType(graphene.Union):
    class Meta:
        types = (ProductType, ErrorType)


class CategoryResponseType(graphene.Union):
    class Meta:
        types = (CategoryType, ErrorType)


class ProductVariationResponseType(graphene.Union):
    class Meta:
        types = (ProductVariationType, ErrorType)

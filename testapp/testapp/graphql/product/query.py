import graphene
from .types.product_types import ProductType, CategoryType, ProductVariationType
from .types.response_types import ProductResponseType, CategoryResponseType
from ..common.common_types import ErrorType
from ...product.models import ProductModel, CategoryModel, ProductVariationModel


###########################################################################
# Queries
###########################################################################
class ProductQueries(graphene.ObjectType):
    products = graphene.List(ProductType, name=graphene.Argument(graphene.String))
    product = graphene.Field(ProductResponseType, id=graphene.ID())
    product_variations = graphene.List(ProductVariationType, product_id=graphene.Argument(graphene.ID))

    @staticmethod
    def resolve_products(self, info, **kwargs):
        if "name" in kwargs:
            name = kwargs['name']
            return ProductModel.objects.filter(name__contains=name)
        else:
            return ProductModel.objects.all()

    @staticmethod
    def resolve_product(self, info, **kwargs):
        _id = kwargs.get('id')
        try:
            return ProductModel.objects.get(pk=_id)
        except ProductModel.DoesNotExist:
            return ErrorType(error_code="NOT_EXIST", error_message="Product does not exist...")


class ProductVariationQueries(graphene.ObjectType):
    product_variations = graphene.List(ProductVariationType, product_id=graphene.Argument(graphene.ID, required=True))
    product_variation = graphene.Field(ProductVariationType, id=graphene.ID())

    @staticmethod
    def resolve_product_variations(self, info, **kwargs):
        product_id = kwargs['product_id']
        return ProductVariationModel.objects.filter(product_id=product_id)

    @staticmethod
    def resolve_product_variation(self, info, **kwargs):
        _id = kwargs.get('id')
        try:
            return ProductVariationModel.objects.get(pk=_id)
        except ProductVariationModel.DoesNotExist:
            return ErrorType(error_code="NOT_EXIST", error_message="Product variation does not exist...")


class CategoryQueries(graphene.ObjectType):
    categories = graphene.List(CategoryType, name=graphene.Argument(graphene.String))
    category = graphene.Field(CategoryResponseType, id=graphene.ID())

    @staticmethod
    def resolve_categories(self, info, **kwargs):
        if "name" in kwargs:
            name = kwargs['name']
            return CategoryModel.objects.filter(name__contains=name)
        else:
            return CategoryModel.objects.all()

    @staticmethod
    def resolve_category(self, info, **kwargs):
        _id = kwargs.get('id')
        try:
            return CategoryModel.objects.get(pk=_id)
        except CategoryModel.DoesNotExist:
            return ErrorType(error_code="NOT_EXIST", error_message="Category does not exist...")

import graphene
from .types.product_types import ProductType, ProductResponseType, ErrorType
from ...product.models import ProductModel


###########################################################################
# Queries
###########################################################################
class ProductQueries(graphene.ObjectType):
    products = graphene.List(ProductType, name=graphene.Argument(graphene.String))
    product = graphene.Field(ProductResponseType, id=graphene.ID())

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

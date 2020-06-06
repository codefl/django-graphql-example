import graphene
from graphene_django import DjangoObjectType
from ....product.models import ProductModel


###########################################################################
# Types
###########################################################################

class ProductType(DjangoObjectType):
    class Meta:
        model = ProductModel


class ErrorType(graphene.ObjectType):
    error_code = graphene.String()
    error_message = graphene.String()


class ProductResponseType(graphene.Union):
    class Meta:
        types = (ProductType, ErrorType)


import graphene
from graphene_django import DjangoConnectionField
from .types.product_types import ProductType, CategoryType, ProductVariationType, TagType
from ...product.models import ProductModel, CategoryModel, ProductVariationModel, TagModel


###########################################################################
# Queries
###########################################################################
class ProductQueries(graphene.ObjectType):
    products = DjangoConnectionField(ProductType, name=graphene.Argument(graphene.String))
    product = graphene.Node.Field(ProductType, id=graphene.Argument(graphene.Int, required=True))

    @staticmethod
    def resolve_products(self, info, **kwargs):
        if "name" in kwargs:
            name = kwargs['name']
            return ProductModel.objects.filter(name__contains=name)
        else:
            return ProductModel.objects.all()


class ProductVariationQueries(graphene.ObjectType):
    product_variations = DjangoConnectionField(ProductVariationType, product_id=graphene.Argument(graphene.Int, required=True))
    product_variation = graphene.Node.Field(ProductVariationType, id=graphene.Argument(graphene.Int, required=True))

    @staticmethod
    def resolve_product_variations(self, info, **kwargs):
        product_id = kwargs['product_id']
        return ProductVariationModel.objects.filter(product_id=product_id)


class CategoryQueries(graphene.ObjectType):
    categories = DjangoConnectionField(CategoryType, name=graphene.Argument(graphene.String))
    category = graphene.Node.Field(CategoryType, id=graphene.Argument(graphene.Int, required=True))

    @staticmethod
    def resolve_categories(self, info, **kwargs):
        if "name" in kwargs:
            name = kwargs['name']
            return CategoryModel.objects.filter(name__contains=name)
        else:
            return CategoryModel.objects.all()


class TagQueries(graphene.ObjectType):
    tags = DjangoConnectionField(TagType, name=graphene.Argument(graphene.String))
    tag = graphene.Node.Field(TagType, id=graphene.Argument(graphene.Int, required=True))

    @staticmethod
    def resolve_tags(self, info, **kwargs):
        if "name" in kwargs:
            name = kwargs['name']
            return TagModel.objects.filter(name__contains=name)
        else:
            return TagModel.objects.all()

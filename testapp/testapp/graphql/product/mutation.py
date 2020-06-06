import graphene
from .mutations.product_mutations import CreateProductMutation


class ProductMutations(graphene.ObjectType):
    create_product = CreateProductMutation.Field()

import graphene
from .product.mutation import ProductMutations
from .product.query import ProductQueries, ProductVariationQueries, CategoryQueries


class Query (
    ProductQueries,
    ProductVariationQueries,
    CategoryQueries,
):
    pass


class Mutation (
    ProductMutations,
):
    pass

schema = graphene.Schema(query=Query, mutation=Mutation)

import graphene
from .product.mutation import ProductMutations, CategoryMutations, ProductVariationMutations
from .product.query import ProductQueries, ProductVariationQueries, CategoryQueries


class Query (
    ProductQueries,
    ProductVariationQueries,
    CategoryQueries,
):
    pass


class Mutation (
    ProductMutations,
    CategoryMutations,
    ProductVariationMutations,
):
    pass

schema = graphene.Schema(query=Query, mutation=Mutation)

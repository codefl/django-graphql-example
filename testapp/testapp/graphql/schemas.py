import graphene
from .product.mutation import ProductMutations, CategoryMutations, ProductVariationMutations, TagMutations
from .product.query import ProductQueries, ProductVariationQueries, CategoryQueries, TagQueries
from .jwt_mutations import JwtMutations


class Query (
    ProductQueries,
    ProductVariationQueries,
    CategoryQueries,
    TagQueries,
):
    pass


class Mutation (
    ProductMutations,
    CategoryMutations,
    ProductVariationMutations,
    TagMutations,
    JwtMutations,
):
    pass


schema = graphene.Schema(query=Query, mutation=Mutation)

import graphene
from .product.mutation import ProductMutations
from .product.query import ProductQueries


class Query (
    ProductQueries,
):
    pass


class Mutation (
    ProductMutations,
):
    pass

schema = graphene.Schema(query=Query, mutation=Mutation)


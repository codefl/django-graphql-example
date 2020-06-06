import graphene
from .mutations.product_mutations import CreateProductMutation, UpdateProductMutation, DeleteProductMutation
from .mutations.category_mutations import CreateCategoryMutation, UpdateCategoryMutation, DeleteCategoryMutation


class ProductMutations(graphene.ObjectType):
    create_product = CreateProductMutation.Field()
    update_product = UpdateProductMutation.Field()
    delete_product = DeleteProductMutation.Field()


class CategoryMutations(graphene.ObjectType):
    create_category = CreateCategoryMutation.Field()
    update_category = UpdateCategoryMutation.Field()
    delete_category = DeleteCategoryMutation.Field()


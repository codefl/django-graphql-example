import graphene
from .mutations.product_mutations import CreateProductMutation, UpdateProductMutation, DeleteProductMutation
from .mutations.category_mutations import CreateCategoryMutation, UpdateCategoryMutation, DeleteCategoryMutation
from .mutations.product_variation_mutations import CreateProductVariationMutation, UpdateProductVariationMutation
from .mutations.product_variation_mutations import DeleteProductVariationMutation


class ProductMutations(graphene.ObjectType):
    create_product = CreateProductMutation.Field()
    update_product = UpdateProductMutation.Field()
    delete_product = DeleteProductMutation.Field()


class CategoryMutations(graphene.ObjectType):
    create_category = CreateCategoryMutation.Field()
    update_category = UpdateCategoryMutation.Field()
    delete_category = DeleteCategoryMutation.Field()


class ProductVariationMutations(graphene.ObjectType):
    create_product_variation = CreateProductVariationMutation.Field()
    update_product_variation = UpdateProductVariationMutation.Field()
    delete_product_variation = DeleteProductVariationMutation.Field()

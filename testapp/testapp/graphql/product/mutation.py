import graphene
from .mutations.product_mutations import CreateProductMutation, UpdateProductMutation, DeleteProductMutation
from .mutations.product_mutations import ProductAddTagMutation, ProductRemoveTagMutation
from .mutations.category_mutations import CreateCategoryMutation, UpdateCategoryMutation, DeleteCategoryMutation
from .mutations.product_variation_mutations import CreateProductVariationMutation, UpdateProductVariationMutation
from .mutations.product_variation_mutations import DeleteProductVariationMutation
from .mutations.tag_mutations import CreateTagMutation, UpdateTagMutation, DeleteTagMutation


class ProductMutations(graphene.ObjectType):
    create_product = CreateProductMutation.Field()
    update_product = UpdateProductMutation.Field()
    delete_product = DeleteProductMutation.Field()
    add_product_tags = ProductAddTagMutation.Field()
    remove_product_tags = ProductRemoveTagMutation.Field()


class CategoryMutations(graphene.ObjectType):
    create_category = CreateCategoryMutation.Field()
    update_category = UpdateCategoryMutation.Field()
    delete_category = DeleteCategoryMutation.Field()


class ProductVariationMutations(graphene.ObjectType):
    create_product_variation = CreateProductVariationMutation.Field()
    update_product_variation = UpdateProductVariationMutation.Field()
    delete_product_variation = DeleteProductVariationMutation.Field()


class TagMutations(graphene.ObjectType):
    create_tag = CreateTagMutation.Field()
    update_tag = UpdateTagMutation.Field()
    delete_tag = DeleteTagMutation.Field()

import graphene
from ..types.response_types import ProductResponseType
from ...common.common_types import ErrorType
from ....product.models import ProductModel, CategoryModel, TagModel
from django.db import models


###########################################################################
# DTO & Response
###########################################################################
class ProductCreateInput(graphene.InputObjectType):
    name = graphene.String(required=True)
    description = graphene.String()
    category_id = graphene.Int()


class ProductUpdateInput(graphene.InputObjectType):
    name = graphene.String()
    description = graphene.String()
    category_id = graphene.Int()


###########################################################################
# Mutations
###########################################################################
class CreateProductMutation(graphene.Mutation):
    class Arguments:
        product_data = graphene.Argument(ProductCreateInput, required=True)

    ok = graphene.Boolean()
    response = graphene.Field(ProductResponseType)

    @staticmethod
    def mutate(root, info, product_data):
        cnt = ProductModel.objects.filter(name__exact=product_data.name).count()

        if cnt > 0:
            r = ErrorType(error_code="DUPLICATE_PRODUCT",
                          error_message="Product {} already exists".format(product_data.name))
            return CreateProductMutation(ok=False, response=r)
        else:
            category = None
            if product_data.category_id is not None:
                try:
                    category = CategoryModel.objects.get(pk=product_data.category_id)
                except CategoryModel.DoesNotExist:
                    r = ErrorType(error_code="CATEGORY_NOT_EXIST",
                                  error_message="Category {} does not exist".format(product_data.category_id))
                    return CreateProductMutation(ok=False, response=r)

            p = ProductModel(name=product_data.name, description=product_data.description, category=category)
            p.save()
            return CreateProductMutation(ok=True, response=p)


class UpdateProductMutation(graphene.Mutation):
    class Arguments:
        product_data = graphene.Argument(ProductUpdateInput, required=True)
        product_id = graphene.ID()

    ok = graphene.Boolean()
    response = graphene.Field(ProductResponseType)

    @staticmethod
    def mutate(root, info, product_id, product_data):
        try:
            product = ProductModel.objects.get(pk=product_id)

            if product_data.name is not None:
                product.name = product_data.name
            if product_data.description is not None:
                product.description = product_data.description
            if product_data.category_id is not None:
                try:
                    category = CategoryModel.objects.get(pk=product_data.category_id)
                    product.category = category
                except CategoryModel.DoesNotExist:
                    r = ErrorType(error_code="CATEGORY_NOT_EXIST",
                                  error_message="Category {} does not exist".format(product_data.category_id))
                    return CreateProductMutation(ok=False, response=r)

            product.save()

            return CreateProductMutation(ok=True, response=product)
        except ProductModel.DoesNotExist:
            r = ErrorType(error_code="PRODUCT_NOT_EXIST",
                          error_message="Product with id {} does not exists".format(product_id))
            return UpdateProductMutation(ok=False, response=r)


class DeleteProductMutation(graphene.Mutation):
    class Arguments:
        product_id = graphene.Int(required=True)

    ok = graphene.Boolean()
    response = graphene.Field(ProductResponseType)

    @staticmethod
    def mutate(root, info, product_id):
        try:
            product = ProductModel.objects.get(pk=product_id)
            product.delete()
            product.id = product_id
            return CreateProductMutation(ok=True, response=product)
        except ProductModel.DoesNotExist:
            r = ErrorType(error_code="PRODUCT_NOT_EXIST",
                          error_message="Product with id {} does not exists".format(product_id))
            return UpdateProductMutation(ok=False, response=r)
        except models.ProtectedError:
            r = ErrorType(error_code="PRODUCT_NOT_DELETE",
                          error_message="Product with id {} cannot be deleted due to dependencies.".format(product_id))
            return UpdateProductMutation(ok=False, response=r)


class ProductAddTagMutation(graphene.Mutation):
    class Arguments:
        product_id = graphene.Int(required=True)
        tag_ids = graphene.List(graphene.Int, required=True)

    ok = graphene.Boolean()
    response = graphene.Field(ErrorType)

    @staticmethod
    def mutate(root, info, product_id, tag_ids):
        try:
            product = ProductModel.objects.get(pk=product_id)
            product_tags = list(product.tags.all())
            tags = TagModel.objects.filter(pk__in=tag_ids)

            tags_to_add = []
            for tag in tags:
                found = False
                for t in product_tags:
                    if t.id == tag.id:
                        found = True
                        break
                if not found:
                    tags_to_add.append(tag)

            # Add tags to product tags
            if len(tags_to_add) > 0:
                product.tags.add(*tags_to_add)

            return ProductAddTagMutation(ok=True)
        except ProductModel.DoesNotExist:
            r = ErrorType(error_code="PRODUCT_NOT_EXIST",
                          error_message="Product with id {} does not exists".format(product_id))
            return UpdateProductMutation(ok=False, response=r)


class ProductRemoveTagMutation(graphene.Mutation):
    class Arguments:
        product_id = graphene.Int(required=True)
        tag_ids = graphene.List(graphene.Int, required=True)

    ok = graphene.Boolean()
    response = graphene.Field(ErrorType)

    @staticmethod
    def mutate(root, info, product_id, tag_ids):
        try:
            product = ProductModel.objects.get(pk=product_id)
            tags = list(TagModel.objects.filter(pk__in=tag_ids))

            product.tags.remove(*tags)
            return ProductAddTagMutation(ok=True)
        except ProductModel.DoesNotExist:
            r = ErrorType(error_code="PRODUCT_NOT_EXIST",
                          error_message="Product with id {} does not exists".format(product_id))
            return UpdateProductMutation(ok=False, response=r)

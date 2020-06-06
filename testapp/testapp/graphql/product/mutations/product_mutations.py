import graphene
from ..types.response_types import ProductResponseType
from ...common.common_types import ErrorType
from ....product.models import ProductModel
from django.db import models


###########################################################################
# DTO & Response
###########################################################################
class ProductInput(graphene.InputObjectType):
    name = graphene.String(required=True)
    description = graphene.String(required=False)
    sku_no = graphene.String(required=True)


###########################################################################
# Mutations
###########################################################################
class CreateProductMutation(graphene.Mutation):
    class Arguments:
        product_data = graphene.Argument(ProductInput, required=True)

    ok = graphene.Boolean()
    response = graphene.Field(ProductResponseType)

    @staticmethod
    def mutate(root, info, product_data):
        cnt = ProductModel.objects.filter(sku_no__exact=product_data.sku_no).count()

        if cnt > 0:
            r = ErrorType(error_code="DUPLICATE_PRODUCT",
                          error_message="Product with sku_no {} already exists".format(product_data.sku_no))

            return CreateProductMutation(ok=False, response=r)
        else:
            p = ProductModel(name=product_data.name, description=product_data.description, sku_no=product_data.sku_no)
            p.save()
            return CreateProductMutation(ok=True, response=p)


class UpdateProductMutation(graphene.Mutation):
    class Arguments:
        product_data = graphene.Argument(ProductInput, required=True)
        product_id = graphene.Argument(graphene.ID(), required=True)

    ok = graphene.Boolean()
    response = graphene.Field(ProductResponseType)

    @staticmethod
    def mutate(root, info, product_id, product_data):
        try:
            product = ProductModel.objects.get(pk=product_id)

            if product_data.sku_no is not None:
                product.sku_no = product_data.sku_no
            if product_data.name is not None:
                product.name = product_data.name
            if product_data.description is not None:
                product.description = product_data.description
            product.save()

            return CreateProductMutation(ok=True, response=product)
        except ProductModel.DoesNotExist:
            r = ErrorType(error_code="PRODUCT_NOT_EXIST",
                          error_message="Product with id {} does not exists".format(product_id))
            return UpdateProductMutation(ok=False, response=r)


class DeleteProductMutation(graphene.Mutation):
    class Arguments:
        product_id = graphene.Argument(graphene.ID(), required=True)

    ok = graphene.Boolean()
    response = graphene.Field(ProductResponseType)

    @staticmethod
    def mutate(root, info, product_id):
        try:
            product = ProductModel.objects.get(pk=product_id)
            product.delete()
            return CreateProductMutation(ok=True, response=product)
        except ProductModel.DoesNotExist:
            r = ErrorType(error_code="PRODUCT_NOT_EXIST",
                          error_message="Product with id {} does not exists".format(product_id))
            return UpdateProductMutation(ok=False, response=r)
        except models.ProtectedError:
            r = ErrorType(error_code="PRODUCT_NOT_DELETE",
                          error_message="Product with id {} cannot be deleted due to dependencies.".format(product_id))
            return UpdateProductMutation(ok=False, response=r)

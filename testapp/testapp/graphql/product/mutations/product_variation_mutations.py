import graphene
from graphene.relay import ClientIDMutation
from graphql_relay import from_global_id
from ..types.response_types import ProductVariationResponseType
from ...common.common_types import ErrorType
from ..types import Currency
from ....product.models import ProductModel, ProductVariationModel
from graphql_jwt.decorators import staff_member_required


###########################################################################
# DTO & Response
###########################################################################
class ProductVariationCreateInput(graphene.InputObjectType):
    sku_no = graphene.String(required=True)
    variation = graphene.String(required=True)
    description = graphene.String()
    currency = Currency(required=True)
    price = graphene.Int(required=True)


class ProductVariationUpdateInput(graphene.InputObjectType):
    sku_no = graphene.String()
    variation = graphene.String()
    description = graphene.String()
    currency = Currency()
    price = graphene.Int()


###########################################################################
# Mutations
###########################################################################
class CreateProductVariationMutation(ClientIDMutation):
    class Input:
        product_id = graphene.ID(required=True)
        product_variation_data = graphene.Argument(ProductVariationCreateInput, required=True)

    ok = graphene.Boolean()
    response = graphene.Field(ProductVariationResponseType)

    @classmethod
    @staff_member_required
    def mutate_and_get_payload(cls, root, info, product_id, product_variation_data):
        product_id = from_global_id(product_id)[1]
        cnt = ProductVariationModel.objects.filter(sku_no__exact=product_variation_data.sku_no).count()

        if cnt > 0:
            r = ErrorType(error_code="DUPLICATE_PRODUCT_VARIATION",
                          error_message="Product variation with sku_no {} already exists".format(product_variation_data.sku_no))

            return CreateProductVariationMutation(ok=False, response=r)
        else:
            try:
                p = ProductModel.objects.get(pk=product_id)
                pv = ProductVariationModel(variation=product_variation_data.variation,
                                           sku_no=product_variation_data.sku_no,
                                           description=product_variation_data.description,
                                           currency=product_variation_data.currency,
                                           price=product_variation_data.price,
                                           product=p)
                pv.save()
                return CreateProductVariationMutation(ok=True, response=pv)
            except ProductModel.DoesNotExist:
                r = ErrorType(error_code="PRODUCT_NOT_EXIST",
                              error_message="Product {} does not exist".format(product_variation_data.product_id))

                return CreateProductVariationMutation(ok=False, response=r)


class UpdateProductVariationMutation(ClientIDMutation):
    class Input:
        product_variation_data = graphene.Argument(ProductVariationUpdateInput, required=True)
        product_variation_id = graphene.ID(required=True)

    ok = graphene.Boolean()
    response = graphene.Field(ProductVariationResponseType)

    @classmethod
    @staff_member_required
    def mutate_and_get_payload(cls, root, info, product_variation_id, product_variation_data):
        try:
            product_variation_id = from_global_id(product_variation_id)[1]
            pv = ProductVariationModel.objects.get(pk=product_variation_id)

            if product_variation_data.sku_no is not None:
                pv.sku_no = product_variation_data.sku_no
            if product_variation_data.variation is not None:
                pv.variation = product_variation_data.variation
            if product_variation_data.description is not None:
                pv.description = product_variation_data.description
            if product_variation_data.currency is not None:
                pv.currency = product_variation_data.currency
            if product_variation_data.price is not None:
                pv.price = product_variation_data.price

            pv.save()

            return UpdateProductVariationMutation(ok=True, response=pv)
        except ProductVariationModel.DoesNotExist:
            r = ErrorType(error_code="PRODUCT_VARIATION_NOT_EXIST",
                          error_message="Product variation with id {} does not exists".format(product_variation_id))
            return UpdateProductVariationMutation(ok=False, response=r)


class DeleteProductVariationMutation(ClientIDMutation):
    class Input:
        product_variation_id = graphene.ID(required=True)

    ok = graphene.Boolean()
    response = graphene.Field(ProductVariationResponseType)

    @classmethod
    @staff_member_required
    def mutate_and_get_payload(cls, root, info, product_variation_id):
        try:
            product_variation_id = from_global_id(product_variation_id)[1]
            pv = ProductVariationModel.objects.get(pk=product_variation_id)
            pv.delete()
            pv.id = product_variation_id
            return DeleteProductVariationMutation(ok=True, response=pv)
        except ProductVariationModel.DoesNotExist:
            r = ErrorType(error_code="PRODUCT_VARIATION_NOT_EXIST",
                          error_message="Product variation with id {} does not exists".format(product_variation_id))
            return DeleteProductVariationMutation(ok=False, response=r)

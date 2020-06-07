import graphene
from ..types.response_types import ProductVariationResponseType
from ...common.common_types import ErrorType
from ..types import Currency
from ....product.models import ProductModel, ProductVariationModel
from ....product import Currency as ModelCurrency


###########################################################################
# DTO & Response
###########################################################################
class ProductVariationInput(graphene.InputObjectType):
    sku_no = graphene.String(required=True)
    variation = graphene.String(required=True)
    description = graphene.String(required=False)
    currency = Currency(required=True)
    price = graphene.Int(required=True)
    product_id = graphene.Int(required=True)


class ProductVariationUpdateInput(graphene.InputObjectType):
    sku_no = graphene.String()
    variation = graphene.String()
    description = graphene.String()
    currency = Currency()
    price = graphene.Int()


###########################################################################
# Mutations
###########################################################################
class CreateProductVariationMutation(graphene.Mutation):
    class Arguments:
        product_variation_data = graphene.Argument(ProductVariationInput, required=True)

    ok = graphene.Boolean()
    response = graphene.Field(ProductVariationResponseType)

    @staticmethod
    def mutate(root, info, product_variation_data):
        cnt = ProductVariationModel.objects.filter(sku_no__exact=product_variation_data.sku_no).count()

        if cnt > 0:
            r = ErrorType(error_code="DUPLICATE_PRODUCT_VARIATION",
                          error_message="Product variation with sku_no {} already exists".format(product_variation_data.sku_no))

            return CreateProductVariationMutation(ok=False, response=r)
        else:
            try:
                p = ProductModel.objects.get(pk=product_variation_data.product_id)
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


class UpdateProductVariationMutation(graphene.Mutation):
    class Arguments:
        product_variation_data = graphene.Argument(ProductVariationUpdateInput, required=True)
        product_variation_id = graphene.ID()

    ok = graphene.Boolean()
    response = graphene.Field(ProductVariationResponseType)

    @staticmethod
    def mutate(root, info, product_variation_id, product_variation_data):
        try:
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


class DeleteProductVariationMutation(graphene.Mutation):
    class Arguments:
        product_variation_id = graphene.ID()

    ok = graphene.Boolean()
    response = graphene.Field(ProductVariationResponseType)

    @staticmethod
    def mutate(root, info, product_variation_id):
        try:
            pv = ProductVariationModel.objects.get(pk=product_variation_id)
            pv.delete()
            pv.id = product_variation_id
            return DeleteProductVariationMutation(ok=True, response=pv)
        except ProductVariationModel.DoesNotExist:
            r = ErrorType(error_code="PRODUCT_VARIATION_NOT_EXIST",
                          error_message="Product variation with id {} does not exists".format(product_variation_id))
            return DeleteProductVariationMutation(ok=False, response=r)

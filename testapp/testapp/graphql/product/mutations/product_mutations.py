import graphene
from ..types.product_types import ProductResponseType, ErrorType
from ....product.models import ProductModel


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

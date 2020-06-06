from django.utils.functional import cached_property
from .product.dataloaders.product_dataloaders import CategoryLoader, ProductVariationLoader


class GQLContext:

    def __init__(self, request):
        self.request = request

    @cached_property
    def user(self):
        return self.request.user

    @cached_property
    def categories_by_category_id_loader(self):
        return CategoryLoader()

    @cached_property
    def variations_by_product_id_loader(self):
        return ProductVariationLoader()

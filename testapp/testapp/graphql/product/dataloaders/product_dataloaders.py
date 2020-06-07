from collections import defaultdict
from promise import Promise
from promise.dataloader import DataLoader
from ....product.models import CategoryModel, ProductModel, TagModel, ProductVariationModel


# Load category by category id
class CategoryLoader(DataLoader):

    def batch_load_fn(self, category_ids):
        # Build the defaultdict to make sure it returns None when the category id does not exist
        category_by_category_ids = defaultdict(CategoryModel)

        # Query the database
        for category in CategoryModel.objects.filter(pk__in=category_ids).iterator():
            category_by_category_ids[category.id] = category

        # Construct the result (same order as the request "category_ids")
        result = [category_by_category_ids[category_id] for category_id in category_ids]
        return Promise.resolve(result)


# Load product variations by product id
class ProductVariationLoader(DataLoader):

    def batch_load_fn(self, product_ids):
        # Build the defaultdict to make sure it returns None when the category id does not exist
        variations_by_product_ids = defaultdict(list)

        # Query the database
        for variation in ProductVariationModel.objects.filter(product_id__in=product_ids).iterator():
            variations_by_product_ids[variation.product_id].append(variation)

        # Construct the result (same order as the request "product_ids")
        result = [variations_by_product_ids.get(product_id, []) for product_id in product_ids]
        return Promise.resolve(result)


# Load product by product id
class ProductLoader(DataLoader):

    def batch_load_fn(self, product_ids):
        # Build the defaultdict to make sure it returns None when the product id does not exist
        products_by_product_ids = defaultdict(ProductModel)

        # Query the database
        for product in ProductModel.objects.filter(pk__in=product_ids).iterator():
            products_by_product_ids[product.id] = product

        # Construct the result (same order as the request "product_ids")
        result = [products_by_product_ids[product_id] for product_id in product_ids]
        return Promise.resolve(result)


# Load products by category id
class CategoryProductLoader(DataLoader):

    def batch_load_fn(self, category_ids):
        # Build the defaultdict to make sure it returns None when the category id does not exist
        products_by_category_ids = defaultdict(list)

        # Query the database
        for product in ProductModel.objects.filter(category_id__in=category_ids).iterator():
            products_by_category_ids[product.category_id].append(product)

        # Construct the result (same order as the request "category_ids")
        result = [products_by_category_ids.get(category_id, []) for category_id in category_ids]
        return Promise.resolve(result)


# Load tags by product id
class ProductTagLoader(DataLoader):

    def batch_load_fn(self, product_ids):
        # Query the database
        product_tags = []
        tag_id_set = {}
        for product_tag in TagModel.products.through.objects.filter(productmodel_id__in=product_ids).iterator():
            product_tags.append[(product_tag.productmodel_id, product_tag.tagmodel_id)]
            tag_id_set.add(product_tag.tagmodel_id)

        tags = defaultdict(None)
        for tag in TagModel.objects.filter(pk__in=list(tag_id_set)).iterator():
            tags[tag.id] = tag

        # Build the defaultdict to make sure it returns None when the product id does not exist
        tags_by_product_ids = defaultdict(list)
        for i in range(0, len(product_tags)):
            product_id = product_tags[i][0]
            tag_id = product_tags[i][1]
            tags_by_product_ids[product_id].append(tags[tag_id])

        # Construct the result (same order as the request "product_ids")
        result = [tags_by_product_ids.get(product_id, []) for product_id in product_ids]
        return Promise.resolve(result)

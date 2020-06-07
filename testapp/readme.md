# 1 Setup Django & GraphQL project

### 1.1 Install django & graphene package
```shell script
$ pip install django
$ pip install 'graphene-django>=2.0'
```

### 1.2 Start a project & application

```shell script
$ django-admin startproject <project_name>
$ cd <project_name>
$ python3 manage.py startapp <app_name> 
```

### 1.3 Add GraphQL support to django project

```python
# add to settings.py
INSTALLED_APPS = (
    # ....
    'django.contrib.staticfiles',  # required by GraphiQL
    'graphene_django'
)

GRAPHENE = {
    'SCHEMA': '<path to the schema object>'  # Where your Graphene schema lives
}
```

```python
# add to urls.py
from django.urls import path
from django.views.decorators.csrf import csrf_exempt
from graphene_django.views import GraphQLView

urlpatterns = [
    # ...
    path("graphql", csrf_exempt(GraphQLView.as_view(graphiql=True))),
]
```

# 2 Create Django Model Object


# 3 Expose through GraphQL Implementation

## 3.1 Directory Layout

* graphql
    * app_dir
        * types  --  (directory for all types, including response type)
            * ProductModelType
            * CategoryType
            * ...
        * mutations  --  (directory for all mutation implementation)
            * CreateProductModelMutation
            * UpdateProductModelMutation
            * ...
        * mutation.py  --  (mutation wrapper class)
        * query.py  --  (query class)
    * schemas.py  --  (schema class wraps queries & mutations)


## 3.2 Types

It defines all the types and response types

```python
class ProductType(DjangoObjectType):
    class Meta:
        model = ProductModel


class ErrorType(graphene.ObjectType):
    error_code = graphene.String()
    error_message = graphene.String()


class ProductResponseType(graphene.Union):
    class Meta:
        types = (ProductType, ErrorType)
```

## 3.3 Define Query

```python
class ProductQueries(graphene.ObjectType):
    products = graphene.List(ProductType, name=graphene.Argument(graphene.String))
    product = graphene.Field(ProductResponseType, id=graphene.ID())

    @staticmethod
    def resolve_products(self, info, **kwargs):
        if "name" in kwargs:
            name = kwargs['name']
            return ProductModel.objects.filter(name__contains=name)
        else:
            return ProductModel.objects.all()

    @staticmethod
    def resolve_product(self, info, **kwargs):
        _id = kwargs.get('id')
        try:
            return ProductModel.objects.get(pk=_id)
        except ProductModel.DoesNotExist:
            return ErrorType(error_code="NOT_EXIST", error_message="Product does not exist...")
```

## 3.4 Define Mutations

Define Input Class

```python
class ProductInput(graphene.InputObjectType):
    name = graphene.String(required=True)
    description = graphene.String(required=False)
    sku_no = graphene.String(required=True)
```

Define Mutation Class

```python
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
```

Assemble Mutations

```python
# mutation.py
class ProductMutations(graphene.ObjectType):
    create_product = CreateProductMutation.Field()
```

## 3.5 Define Schema (assemble queries & mutations to schema)

```python
# schemas.py

class Query (
    ProductQueries,
):
    pass


class Mutation (
    ProductMutations,
):
    pass

schema = graphene.Schema(query=Query, mutation=Mutation)
```

# 4 Data Loader

## 4.1 Preparation

Best Practices
* Data loader instance per request
* Add dataloader instance to custom context per request
* Add custom view object to initiate the context

### 4.1.1 Add custom context object

```python
# add context.py with the following content

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
```

### 4.1.2 Add custom view object to initiate the custom context

```python
# Add views.py

from graphene_django.views import GraphQLView
from .context import GQLContext

class CustomGraphQLView(GraphQLView):

    def get_context(self, request):
        return GQLContext(request)
```

### 4.1.3 Wire the custom view object to handle graphql request

```python
# Update urls.py

from django.urls import path
from django.views.decorators.csrf import csrf_exempt
from .graphql.views import CustomGraphQLView

urlpatterns = [
    # ....
    path("graphql", csrf_exempt(CustomGraphQLView.as_view(graphiql=True))),
]
```

## 4.2 Implement Data Loader for each scenarios

### 4.2.1 Example for many to one relation

Load "Category" when requesting "Product"

```python
from collections import defaultdict
from promise import Promise
from promise.dataloader import DataLoader
from ....product.models import CategoryModel

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
```

### 4.2.2 Example for one to many relation

Load "ProductVariation" when requesting "Product"

```python
from collections import defaultdict
from promise import Promise
from promise.dataloader import DataLoader
from ....product.models import ProductVariationModel

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
```

# 5 Many to Many relationship

## 5.1 Define relationship

```python
class TagModel(models.Model):
    name = models.CharField(max_length=100, blank=False)
    description = models.CharField(max_length=100, null=True, blank=True)

    def __str__(self):
        return self.name


class ProductModel(models.Model):
    # .....
    tags = models.ManyToManyField(TagModel, related_name="products")

    def __str__(self):
        return self.name
``` 

## 5.2 Many to Many Table

Many to many table is represented in model:
* TagModel.products.through
* ProductModel.tags.through

The sample query like below:
* TagModel.products.through.filter(productmodel_id__in=[list of product id])
* The result is the relation objects of (productmodel_id, tagmodel_id)

## 5.3 Tags manipulation

Query tags:
* ProductModel.objects.get(pk=product_id).tags.all()

Add tag to product:
* product.tags.add(tag)
* product.tags.add(*tags)

Remove tag from product:
* product.tags.remove(tag)
* product.tags.remove(*tags)


# 6 Others

## 6.1 DB SQL Logging

Add the following snippet to settings.py

```python
if DEBUG:
    import logging

    l = logging.getLogger('django.db.backends')
    l.setLevel(logging.DEBUG)
    l.addHandler(logging.StreamHandler())

LOGGING = {
    'version': 1,
    'filters': {
        'require_debug_true': {
            '()': 'django.utils.log.RequireDebugTrue',
        }
    },
    'handlers': {
        'console': {
            'level': 'DEBUG',
            'filters': ['require_debug_true'],
            'class': 'logging.StreamHandler',
        }
    },
    'loggers': {
        'django.db.backends': {
            'level': 'DEBUG',
            'handlers': ['console'],
        }
    }
}
```
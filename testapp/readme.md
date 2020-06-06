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

# 4 Others

## 4.1 DB SQL Logging

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